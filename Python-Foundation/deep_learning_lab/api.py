import os
import io
import torch
import chromadb
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from ultralytics import YOLO

app = FastAPI(
    title="Multimodal Visual Search API",
    description="Production REST microservice powering text, image, and YOLO-assisted visual retrieval via CLIP and ChromaDB.",
    version="1.0.0",
)

# Device Configuration
device = "cuda" if torch.cuda.is_available() else "cpu"
script_dir = os.path.dirname(os.path.abspath(__file__))
indexed_images_dir = os.path.join(script_dir, "indexed_images")

# Load Vision & Embedding Models
print(f"Loading CLIP model on {device}...")
model_id = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(model_id).to(device)
clip_processor = CLIPProcessor.from_pretrained(model_id)

yolo_path = os.path.join(script_dir, "yolo11n.pt")
yolo_model = YOLO(yolo_path if os.path.exists(yolo_path) else "yolo11n.pt")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path=os.path.join(script_dir, "chroma_visual_db")
)
collection = chroma_client.get_collection(name="cifar_visual_search")


# Pydantic Schemas
class SearchResultItem(BaseModel):
    filename: str
    true_label: str
    similarity_score: float


class TextSearchRequest(BaseModel):
    query: str
    category: Optional[str] = "all"
    top_k: Optional[int] = 4


class SearchResponse(BaseModel):
    query_type: str
    total_matches: int
    results: List[SearchResultItem]


class DetectedObjectMatch(BaseModel):
    object_index: int
    detected_class: str
    confidence: float
    bbox: List[int]
    matches: List[SearchResultItem]


class DetectionSearchResponse(BaseModel):
    total_objects_detected: int
    detections: List[DetectedObjectMatch]


# Helper Embedding & Query Functions
def extract_text_embedding(text: str) -> list:
    with torch.no_grad():
        inputs = clip_processor(text=[text], return_tensors="pt", padding=True).to(
            device
        )
        outputs = clip_model.get_text_features(**inputs)
        features = (
            outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
        )
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy().tolist()


def extract_image_embedding(image: Image.Image) -> list:
    with torch.no_grad():
        inputs = clip_processor(images=image.convert("RGB"), return_tensors="pt").to(
            device
        )
        outputs = clip_model.get_image_features(**inputs)
        features = (
            outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
        )
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy().tolist()


def query_chromadb(
    embedding: list, category_filter: Optional[str], top_k: int
) -> List[SearchResultItem]:
    where_filter = (
        None
        if (not category_filter or category_filter == "all")
        else {"true_label": category_filter}
    )

    res = collection.query(
        query_embeddings=embedding,
        n_results=top_k,
        where=where_filter,
        include=["metadatas", "distances"],
    )

    matches = []
    if res["metadatas"] and len(res["metadatas"][0]) > 0:
        for meta, dist in zip(res["metadatas"][0], res["distances"][0]):
            matches.append(
                SearchResultItem(
                    filename=meta["filename"],
                    true_label=meta["true_label"],
                    similarity_score=round((1.0 - dist) * 100, 2),
                )
            )
    return matches


# API Endpoints
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "device": device,
        "indexed_vectors": collection.count(),
        "collection_name": collection.name,
    }


@app.post("/search/text", response_model=SearchResponse)
def search_text(payload: TextSearchRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Text query cannot be empty.")

    embedding = extract_text_embedding(payload.query)
    matches = query_chromadb(embedding, payload.category, payload.top_k)
    return SearchResponse(
        query_type="text", total_matches=len(matches), results=matches
    )


@app.post("/search/image", response_model=SearchResponse)
async def search_image(
    file: UploadFile = File(...),
    category: Optional[str] = Form("all"),
    top_k: Optional[int] = Form(4),
):
    try:
        contents = await file.read()
        pil_image = Image.open(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image payload.")

    embedding = extract_image_embedding(pil_image)
    matches = query_chromadb(embedding, category, top_k)
    return SearchResponse(
        query_type="image", total_matches=len(matches), results=matches
    )


@app.post("/search/detect-and-search", response_model=DetectionSearchResponse)
async def detect_and_search_endpoint(
    file: UploadFile = File(...),
    category: Optional[str] = Form("all"),
    top_k: Optional[int] = Form(4),
):
    try:
        contents = await file.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image payload.")

    # Execute YOLO object localization
    results = yolo_model(pil_image)
    boxes = results[0].boxes

    detected_matches = []

    for idx, box in enumerate(boxes, 1):
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cls_id = int(box.cls[0].item())
        cls_name = yolo_model.names.get(cls_id, "object")
        conf = round(float(box.conf[0].item()), 3)

        # Crop the localized bounding box region
        crop = pil_image.crop((x1, y1, x2, y2))

        # Extract visual feature vector and query database
        crop_embedding = extract_image_embedding(crop)
        matches = query_chromadb(crop_embedding, category, top_k)

        detected_matches.append(
            DetectedObjectMatch(
                object_index=idx,
                detected_class=cls_name,
                confidence=conf,
                bbox=[x1, y1, x2, y2],
                matches=matches,
            )
        )

    return DetectionSearchResponse(
        total_objects_detected=len(detected_matches), detections=detected_matches
    )
