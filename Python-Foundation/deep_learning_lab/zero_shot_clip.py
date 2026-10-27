import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# 1. Device and Model Initialization
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Loading CLIP on: {device}...")

# Load pretrained CLIP (ViT-B/32 backbone)
model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

# 2. Define Open-Vocabulary Candidate Labels
# You can supply standard CIFAR classes alongside true descriptive candidates
candidate_labels = [
    "an airplane in the sky",
    "an automobile on the road",
    "a cartoon character walking in the snow",
    "a video game illustration",
    "a bird",
    "a cat",
]

# 3. Load the Query Image
img_path = "download.jpg"  # Or your uploaded image file
image = Image.open(img_path).convert("RGB")

# 4. Multimodal Preprocessing & Tokenization
inputs = processor(
    text=candidate_labels, images=image, return_tensors="pt", padding=True
).to(device)

# 5. Compute Shared Embeddings & Cosine Similarities
with torch.no_grad():
    outputs = model(**inputs)
    # outputs.logits_per_image computes the scaled cosine similarity between image and text embeddings
    logits_per_image = outputs.logits_per_image
    probabilities = logits_per_image.softmax(dim=1)[0]

# 6. Display Ranked Predictions
results = sorted(
    zip(candidate_labels, probabilities.cpu().tolist()),
    key=lambda x: x[1],
    reverse=True,
)

print("\n" + "=" * 55)
print(f" CLIP Zero-Shot Classification Results")
print("=" * 55)
for label, score in results:
    bar = "█" * int(score * 30)
    print(f"{label:<40} | {score * 100:6.2f}% {bar}")
print("=" * 55)
