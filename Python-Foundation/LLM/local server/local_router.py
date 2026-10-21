import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np

print("🔄 Initializing Local Jev Engine...")
model_name = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto", device_map="auto"
)


class LocalJev:
    @staticmethod
    def _get_logits(state, prompt_suffix):
        prompt = f"Context: {state}\nQuestion: {prompt_suffix}"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.logits[0, -1, :]

    @classmethod
    def choice(cls, state, options):
        """Replicates Jev's parallel categorization feature"""
        next_token_logits = cls._get_logits(
            state, f"Which option best fits? Options: {', '.join(options)}. Answer:"
        )
        scores = []
        for opt in options:
            token_ids = tokenizer.encode(opt, add_special_tokens=False)
            scores.append(next_token_logits[token_ids[0]].item())

        exp_scores = np.exp(scores - np.max(scores))
        probs = exp_scores / exp_scores.sum()

        probabilities_dict = {opt: float(p) for opt, p in zip(options, probs)}
        best_choice = max(probabilities_dict, key=probabilities_dict.get)
        return {
            "choice": best_choice,
            "confidence": probabilities_dict[best_choice],
            "probabilities": probabilities_dict,
        }

    @classmethod
    def noul(cls, state, statement):
        """Replicates Jev's binary calibrated probability function"""
        next_token_logits = cls._get_logits(
            state,
            f"Is this statement true or false? Statement: '{statement}'. Answer (Yes/No):",
        )

        yes_id = tokenizer.encode("Yes", add_special_tokens=False)
        no_id = tokenizer.encode("No", add_special_tokens=False)

        scores = [
            next_token_logits[yes_id[0]].item(),
            next_token_logits[no_id[0]].item(),
        ]
        exp_scores = np.exp(scores - np.max(scores))
        probs = exp_scores / exp_scores.sum()

        # FIX: Extract the first array item [0] representing the 'Yes' value
        return {"noul": float(probs[0])}

    @classmethod
    def score(cls, state, rubric):
        """Replicates Jev's probability-weighted custom scoring scales"""
        levels = list(rubric.keys())
        rubric_str = " ".join([f"[{k}] {v}" for k, v in rubric.items()])
        next_token_logits = cls._get_logits(
            state, f"Rate this based on the rubric: {rubric_str}. Numerical rating:"
        )

        scores = []
        for lvl in levels:
            token_id = tokenizer.encode(str(lvl), add_special_tokens=False)
            scores.append(next_token_logits[token_id[0]].item())

        exp_scores = np.exp(scores - np.max(scores))
        probs = exp_scores / exp_scores.sum()

        weighted_score = sum(int(lvl) * p for lvl, p in zip(levels, probs))
        probabilities_dict = {lvl: float(p) for lvl, p in zip(levels, probs)}
        return {
            "score": float(round(weighted_score, 2)),
            "probabilities": probabilities_dict,
        }


# ==========================================
# 🚀 PROD TEST RUN
# ==========================================
ticket = (
    "Hey! My credit card was billed twice for transaction #5502. Fix this immediately!"
)

print("\n--- Running Clean Choice Primitive ---")
print(LocalJev.choice(ticket, ["billing", "tech_support", "sales"]))

print("\n--- Running Clean Noul Primitive ---")
print(LocalJev.noul(ticket, "The user is angry or expressing urgency"))

print("\n--- Running Clean Score Primitive ---")
rubric_scale = {"1": "Calm query.", "2": "Frustrated.", "3": "Absolute emergency."}
print(LocalJev.score(ticket, rubric_scale))
