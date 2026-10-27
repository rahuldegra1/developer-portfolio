import os
import time
import torch
import numpy as np
from PIL import Image
import chromadb
from transformers import CLIPProcessor, CLIPModel
from ultralytics import YOLO
import onnxruntime as ort

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Profiling environment: PyTorch {torch.__version__} | Primary Device: {device}")

script_dir = os.path.dirname(os.path.abspath(__file__))
indexed_dir = os.path.join(script_dir, "indexed_images")
onnx_path = os.path.join(script_dir, "clip_visual.onnx")

# Load models
model_id = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

yolo_weight = os.path.join(script_dir, "yolo11n.pt")
yolo_model = YOLO(yolo_weight if os.path.exists(yolo_weight) else "yolo11n.pt")

chroma_client = chromadb.PersistentClient(
    path=os.path.join(script_dir, "chroma_visual_db")
)
collection = chroma_client.get_collection(name="cifar_visual_search")

# Dummy input data
test_img_path = os.path.join(indexed_dir, os.listdir(indexed_dir)[0])
test_image = Image.open(test_img_path).convert("RGB")
test_text = "a fast vehicle driving on the highway"

# -------------------------------------------------------------
# Part 1: End-to-End Pipeline Latency Breakdown (PyTorch)
# -------------------------------------------------------------
print("\n" + "=" * 65)
print(" 1. COMPONENT-LEVEL LATENCY PROFILING (10 ITERATIONS)")
print("=" * 65)

ITERATIONS = 10

# 1.1 YOLO Detection
times_yolo = []
for _ in range(ITERATIONS):
    t0 = time.perf_counter()
    _ = yolo_model(test_image, verbose=False)
    if device == "cuda":
        torch.cuda.synchronize()
    times_yolo.append((time.perf_counter() - t0) * 1000)

# 1.2 CLIP Text Encoding
times_clip_text = []
for _ in range(ITERATIONS):
    t0 = time.perf_counter()
    inputs = processor(text=[test_text], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        out = clip_model.get_text_features(**inputs)
        feats = out.pooler_output if hasattr(out, "pooler_output") else out
        _ = feats / feats.norm(dim=-1, keepdim=True)
    if device == "cuda":
        torch.cuda.synchronize()
    times_clip_text.append((time.perf_counter() - t0) * 1000)

# 1.3 CLIP Vision Encoding (PyTorch)
times_clip_vision = []
for _ in range(ITERATIONS):
    t0 = time.perf_counter()
    inputs = processor(images=test_image, return_tensors="pt").to(device)
    with torch.no_grad():
        out = clip_model.get_image_features(**inputs)
        feats = out.pooler_output if hasattr(out, "pooler_output") else out
        norm_feats = feats / feats.norm(dim=-1, keepdim=True)
    if device == "cuda":
        torch.cuda.synchronize()
    times_clip_vision.append((time.perf_counter() - t0) * 1000)

dummy_embedding = norm_feats.cpu().numpy().tolist()

# 1.4 ChromaDB HNSW Cosine Search (5,000 vectors)
times_chroma = []
for _ in range(ITERATIONS):
    t0 = time.perf_counter()
    _ = collection.query(
        query_embeddings=dummy_embedding, n_results=4, include=["distances"]
    )
    times_chroma.append((time.perf_counter() - t0) * 1000)

print(
    f"YOLO11 Detection Latency        : {np.mean(times_yolo):6.2f} ms ± {np.std(times_yolo):.2f} ms"
)
print(
    f"CLIP Text Feature Extraction    : {np.mean(times_clip_text):6.2f} ms ± {np.std(times_clip_text):.2f} ms"
)
print(
    f"CLIP Vision Feature Extraction  : {np.mean(times_clip_vision):6.2f} ms ± {np.std(times_clip_vision):.2f} ms"
)
print(
    f"ChromaDB Query (5,000 index)    : {np.mean(times_chroma):6.2f} ms ± {np.std(times_chroma):.2f} ms"
)
total_pipeline_ms = (
    np.mean(times_yolo) + np.mean(times_clip_vision) + np.mean(times_chroma)
)
print(
    f"Total Detect + Embed + Query    : {total_pipeline_ms:6.2f} ms (~{1000 / total_pipeline_ms:.1f} FPS)"
)

# -------------------------------------------------------------
# Part 2: ONNX Export for CLIP Vision Model
# -------------------------------------------------------------
print("\n" + "=" * 65)
print(" 2. EXPORTING CLIP VISION ENCODER TO ONNX")
print("=" * 65)


class CLIPVisionWrapper(torch.nn.Module):
    def __init__(self, visual_model):
        super().__init__()
        self.visual = visual_model

    def forward(self, pixel_values):
        feats = self.visual(pixel_values=pixel_values)
        out = feats.pooler_output if hasattr(feats, "pooler_output") else feats[1]
        return out / out.norm(dim=-1, keepdim=True)


wrapper = CLIPVisionWrapper(clip_model.vision_model).cpu().eval()
dummy_pixel_values = torch.randn(1, 3, 224, 224)

if not os.path.exists(onnx_path):
    print("Tracing and exporting model graph to ONNX...")
    torch.onnx.export(
        wrapper,
        dummy_pixel_values,
        onnx_path,
        input_names=["pixel_values"],
        output_names=[
            "visual_features"
        ],  # Renamed to avoid internal CLIP naming collision
        dynamic_axes={
            "pixel_values": {0: "batch_size"},
            "visual_features": {0: "batch_size"},
        },
        opset_version=14,
    )
    print(
        f"Saved ONNX model to: {onnx_path} ({os.path.getsize(onnx_path) / (1024 * 1024):.1f} MB)"
    )
else:
    print(f"Found existing ONNX model at: {onnx_path}")

# -------------------------------------------------------------
# Part 3: ONNX Runtime vs PyTorch Latency Comparison
# -------------------------------------------------------------
print("\n" + "=" * 65)
print(" 3. ONNX RUNTIME VS PYTORCH BENCHMARK (CPU RUNTIME)")
print("=" * 65)

ort_session = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
ort_inputs = {"pixel_values": dummy_pixel_values.numpy()}

# Warmup
for _ in range(3):
    _ = wrapper(dummy_pixel_values)
    _ = ort_session.run(None, ort_inputs)

# PyTorch CPU benchmark
pt_cpu_times = []
for _ in range(ITERATIONS):
    t0 = time.perf_counter()
    with torch.no_grad():
        _ = wrapper(dummy_pixel_values)
    pt_cpu_times.append((time.perf_counter() - t0) * 1000)

# ONNX Runtime CPU benchmark
ort_times = []
for _ in range(ITERATIONS):
    t0 = time.perf_counter()
    _ = ort_session.run(None, ort_inputs)
    ort_times.append((time.perf_counter() - t0) * 1000)

print(f"PyTorch CPU Latency      : {np.mean(pt_cpu_times):6.2f} ms")
print(f"ONNX Runtime CPU Latency : {np.mean(ort_times):6.2f} ms")
speedup = np.mean(pt_cpu_times) / np.mean(ort_times)
print(f"ONNX Runtime Speedup     : {speedup:.2f}x faster on CPU")
print("=" * 65)
