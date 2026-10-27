import os
import torch
import chromadb
from torchvision.datasets import CIFAR10
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading CLIP embedding model on: {device}...")

model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

script_dir = os.path.dirname(os.path.abspath(__file__))
indexed_dir = os.path.join(script_dir, "indexed_images")
os.makedirs(indexed_dir, exist_ok=True)

# ChromaDB Setup
chroma_client = chromadb.PersistentClient(
    path=os.path.join(script_dir, "chroma_visual_db")
)
collection = chroma_client.get_or_create_collection(
    name="cifar_visual_search", metadata={"hnsw:space": "cosine"}
)
SAMPLE_COUNT = 5000
BATCH_SIZE = 128

# Reset collection to re-index with the larger count
chroma_client.delete_collection(name="cifar_visual_search")
collection = chroma_client.create_collection(
    name="cifar_visual_search", metadata={"hnsw:space": "cosine"}
)

print(f"Populating vector index from CIFAR-10 test set ({SAMPLE_COUNT} samples)...")
test_set = CIFAR10(
    root=os.path.join(script_dir, "data_cifar"), train=False, download=True
)

for batch_start in range(0, SAMPLE_COUNT, BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE, SAMPLE_COUNT)
    batch_images = []
    batch_ids = []
    batch_meta = []

    for i in range(batch_start, batch_end):
        img, label_idx = test_set[i]
        label_name = test_set.classes[label_idx]

        filename = f"img_{i}_{label_name}.png"
        img.save(os.path.join(indexed_dir, filename))

        batch_images.append(img)
        batch_ids.append(f"doc_{i}")
        batch_meta.append({"filename": filename, "true_label": label_name})

    with torch.no_grad():
        inputs = processor(images=batch_images, return_tensors="pt").to(device)
        outputs = model.get_image_features(**inputs)
        feats = outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
        feats = feats / feats.norm(dim=-1, keepdim=True)
        embeddings = feats.cpu().numpy().tolist()

    collection.add(ids=batch_ids, embeddings=embeddings, metadatas=batch_meta)
    print(f"Indexed [{batch_end}/{SAMPLE_COUNT}] images...")

print("5,000 image index populated successfully.")


def search_by_text(query: str, top_k: int = 3):
    with torch.no_grad():
        inputs = processor(text=[query], return_tensors="pt", padding=True).to(device)
        outputs = model.get_text_features(**inputs)
        text_features = (
            outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
        )
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        query_embedding = text_features.cpu().numpy().tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["metadatas", "distances"],
    )

    print(f"\n{'=' * 60}")
    print(f" TEXT QUERY: '{query}'")
    print("=" * 60)
    for rank, (meta, dist) in enumerate(
        zip(results["metadatas"][0], results["distances"][0]), 1
    ):
        sim = (1.0 - dist) * 100
        print(
            f"Rank {rank}: Label: {meta['true_label']:<10} | Sim: {sim:.2f}% | File: {meta['filename']}"
        )


if __name__ == "__main__":
    search_by_text("an animal with long ears that hops", top_k=3)
    search_by_text("a red vehicle driving fast", top_k=3)
    search_by_text("a bird flying high in the blue sky", top_k=3)
    search_by_text("a massive metal ship in the ocean", top_k=3)
