from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
from pydantic import BaseModel

# 1. Initialize the core FastAPI application
app = FastAPI(title="Local Jev & Coding API Engine")

print("🔄 Initializing Qwen 2.5 7B in background memory...")
model_name = "Qwen/Qwen2.5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto", device_map="auto"
)


# Shared helper function to extract raw logits for classification tasks
def _get_logits(state: str, prompt_suffix: str):
    prompt = f"Context: {state}\nQuestion: {prompt_suffix}"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.logits[0, -1, :]


# --- REQUEST SCHEMAS (Pydantic Models) ---
class ChoiceRequest(BaseModel):
    state: str
    options: List[str]


class NoulRequest(BaseModel):
    state: str
    statement: str


class ScoreRequest(BaseModel):
    state: str
    rubric: Dict[str, str]


class CodeGenerationRequest(BaseModel):
    prompt: str
    language: str = "python"


class RAGRequest(BaseModel):
    prompt: str


# --- CLASSIFICATION ENDPOINTS (System One Style) ---


@app.post("/v1/choice")
def api_choice(req: ChoiceRequest):
    if not req.options:
        raise HTTPException(status_code=400, detail="Options array cannot be empty")
    next_token_logits = _get_logits(
        req.state, f"Which option best fits? Options: {', '.join(req.options)}. Answer:"
    )
    scores = []
    for opt in req.options:
        token_ids = tokenizer.encode(opt, add_special_tokens=False)
        scores.append(next_token_logits[token_ids].item())
    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()
    probabilities_dict = {opt: float(p) for opt, p in zip(req.options, probs)}
    best_choice = max(probabilities_dict, key=probabilities_dict.get)
    return {
        "choice": best_choice,
        "confidence": probabilities_dict[best_choice],
        "probabilities": probabilities_dict,
    }


@app.post("/v1/noul")
def api_noul(req: NoulRequest):
    next_token_logits = _get_logits(
        req.state,
        f"Is this statement true or false? Statement: '{req.statement}'. Answer (Yes/No):",
    )
    yes_id = tokenizer.encode("Yes", add_special_tokens=False)
    no_id = tokenizer.encode("No", add_special_tokens=False)
    scores = [next_token_logits[yes_id].item(), next_token_logits[no_id].item()]
    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()
    return {"noul": float(probs)}


@app.post("/v1/score")
def api_score(req: ScoreRequest):
    levels = list(req.rubric.keys())
    rubric_str = " ".join([f"[{k}] {v}" for k, v in req.rubric.items()])
    next_token_logits = _get_logits(
        req.state, f"Rate this based on the rubric: {rubric_str}. Numerical rating:"
    )
    scores = [
        next_token_logits[tokenizer.encode(str(lvl), add_special_tokens=False)].item()
        for lvl in levels
    ]
    exp_scores = np.exp(scores - np.max(scores))
    probs = exp_scores / exp_scores.sum()
    weighted_score = sum(int(lvl) * p for lvl, p in zip(levels, probs))
    return {
        "score": float(round(weighted_score, 2)),
        "probabilities": {lvl: float(p) for lvl, p in zip(levels, probs)},
    }


# --- NATIVE HIGH-LEVEL CODE GENERATION ENDPOINT (System Two Style) ---


@app.post("/generate_code")
def generate_response(req: RAGRequest):  # Changed 'request' to 'req' to match your code
    user_prompt = req.prompt

    # Replace your old strict system prompt with this conversational one
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Answer the user's question using ONLY the provided context.",
        },
        {"role": "user", "content": user_prompt},
    ]

    # Properly format the special tokens for Qwen 2.5
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    model_inputs = tokenizer([prompt], return_tensors="pt").to(model.device)
    attention_mask = model_inputs.get(
        "attention_mask", torch.ones_like(model_inputs.input_ids)
    )

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=model_inputs.input_ids,
            attention_mask=attention_mask,
            max_new_tokens=1024,
            use_cache=True,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False,
        )

    new_tokens = generated_ids[0][len(model_inputs.input_ids[0]) :]
    generated_code = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    # Structural sanitation: strip code block fences if emitted
    if generated_code.startswith("```"):
        lines = generated_code.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        generated_code = "\n".join(lines).strip()

    return {"response": generated_code}
