import os
import torch
import chromadb
import gradio as gr
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Loading CLIP model on {device}...")

model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

script_dir = os.path.dirname(os.path.abspath(__file__))
indexed_images_dir = os.path.join(script_dir, "indexed_images")

# Load YOLO11
yolo_weight_path = os.path.join(script_dir, "yolo11n.pt")
yolo_model = YOLO(
    yolo_weight_path if os.path.exists(yolo_weight_path) else "yolo11n.pt"
)

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path=os.path.join(script_dir, "chroma_visual_db")
)
collection = chroma_client.get_collection(name="cifar_visual_search")
print(f"Connected to collection. Items loaded: {collection.count()}")

CIFAR_CLASSES = [
    "all",
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def search_by_text(query_text: str, category_filter: str = "all", top_k: int = 4):
    if not query_text.strip():
        return []

    with torch.no_grad():
        inputs = processor(text=[query_text], return_tensors="pt", padding=True).to(
            device
        )
        outputs = model.get_text_features(**inputs)
        features = (
            outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
        )
        features = features / features.norm(dim=-1, keepdim=True)
        query_embedding = features.cpu().numpy().tolist()

    where_filter = None if category_filter == "all" else {"true_label": category_filter}

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where_filter,
        include=["metadatas", "distances"],
    )

    gallery_items = []
    for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
        sim_pct = (1.0 - dist) * 100
        img_path = os.path.join(indexed_images_dir, meta["filename"])
        if os.path.exists(img_path):
            img = Image.open(img_path)
            caption = f"Label: {meta['true_label']} | Sim: {sim_pct:.1f}%"
            gallery_items.append((img, caption))

    print(
        f"Text Query: '{query_text}' | Filter: {category_filter} | Retrieved {len(gallery_items)} images."
    )
    return gallery_items


def search_by_image(
    query_image: Image.Image, category_filter: str = "all", top_k: int = 4
):
    if query_image is None:
        return []

    with torch.no_grad():
        inputs = processor(images=query_image.convert("RGB"), return_tensors="pt").to(
            device
        )
        outputs = model.get_image_features(**inputs)
        features = (
            outputs.pooler_output if hasattr(outputs, "pooler_output") else outputs
        )
        features = features / features.norm(dim=-1, keepdim=True)
        query_embedding = features.cpu().numpy().tolist()

    where_filter = None if category_filter == "all" else {"true_label": category_filter}

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        where=where_filter,
        include=["metadatas", "distances"],
    )

    gallery_items = []
    for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
        sim_pct = (1.0 - dist) * 100
        img_path = os.path.join(indexed_images_dir, meta["filename"])
        if os.path.exists(img_path):
            img = Image.open(img_path)
            caption = f"Label: {meta['true_label']} | Sim: {sim_pct:.1f}%"
            gallery_items.append((img, caption))

    return gallery_items


def process_scene_detections(scene_image: Image.Image):
    if scene_image is None:
        return None, gr.Dropdown(choices=[], value=None), {}

    rgb_img = scene_image.convert("RGB")
    results = yolo_model(rgb_img)

    annotated_bgr = results[0].plot()
    annotated_rgb = Image.fromarray(annotated_bgr[..., ::-1])

    boxes = results[0].boxes
    if len(boxes) == 0:
        return annotated_rgb, gr.Dropdown(choices=[], value=None), {}

    crops_dict = {}
    choices = []

    for idx, box in enumerate(boxes, 1):
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cls_id = int(box.cls[0].item())
        cls_name = yolo_model.names.get(cls_id, "object")
        conf = float(box.conf[0].item())

        crop = rgb_img.crop((x1, y1, x2, y2))
        choice_label = f"Obj {idx}: {cls_name} ({conf:.2f})"

        crops_dict[choice_label] = crop
        choices.append(choice_label)

    first_choice = choices[0] if choices else None
    return annotated_rgb, gr.Dropdown(choices=choices, value=first_choice), crops_dict


def query_selected_crop(
    selected_crop_name: str, crops_dict: dict, category_filter: str, top_k: int
):
    if not selected_crop_name or not crops_dict or selected_crop_name not in crops_dict:
        return None, []

    crop_img = crops_dict[selected_crop_name]
    gallery = search_by_image(crop_img, category_filter=category_filter, top_k=top_k)
    return crop_img, gallery


with gr.Blocks(title="Neural Visual Search") as demo:
    detected_crops_state = gr.State({})

    gr.Markdown("# Multimodal Visual Search Engine (CLIP + ChromaDB + YOLO)")
    gr.Markdown(
        "Search indexed CIFAR-10 images using text, image-to-image similarity, or object detection crops."
    )

    with gr.Tabs():
        with gr.TabItem("Text-to-Image Search"):
            with gr.Row():
                with gr.Column(scale=1):
                    text_input = gr.Textbox(
                        label="Text Prompt",
                        placeholder="e.g. vintage vehicle driving on a road",
                        lines=2,
                    )
                    category_dd1 = gr.Dropdown(
                        choices=CIFAR_CLASSES,
                        value="all",
                        label="Filter by True Class (Metadata Where)",
                    )
                    top_k_slider1 = gr.Slider(
                        minimum=1, maximum=12, value=4, step=1, label="Top Results"
                    )
                    btn_search_text = gr.Button("Search Images", variant="primary")
                with gr.Column(scale=2):
                    text_gallery = gr.Gallery(
                        label="Matched Images", columns=4, height="auto"
                    )

            btn_search_text.click(
                fn=search_by_text,
                inputs=[text_input, category_dd1, top_k_slider1],
                outputs=text_gallery,
            )
            text_input.submit(
                fn=search_by_text,
                inputs=[text_input, category_dd1, top_k_slider1],
                outputs=text_gallery,
            )

        with gr.TabItem("Image-to-Image (Reverse Search)"):
            with gr.Row():
                with gr.Column(scale=1):
                    image_input = gr.Image(type="pil", label="Query Image")
                    category_dd2 = gr.Dropdown(
                        choices=CIFAR_CLASSES,
                        value="all",
                        label="Filter by True Class (Metadata Where)",
                    )
                    top_k_slider2 = gr.Slider(
                        minimum=1, maximum=12, value=4, step=1, label="Top Results"
                    )
                    btn_search_img = gr.Button(
                        "Find Visually Similar", variant="primary"
                    )
                with gr.Column(scale=2):
                    image_gallery = gr.Gallery(
                        label="Closest Neighbors", columns=4, height="auto"
                    )

            btn_search_img.click(
                fn=search_by_image,
                inputs=[image_input, category_dd2, top_k_slider2],
                outputs=image_gallery,
            )

        with gr.TabItem("Detect & Search (YOLO + CLIP)"):
            with gr.Row():
                with gr.Column(scale=1):
                    yolo_input = gr.Image(type="pil", label="Upload Scene Photo")
                    btn_run_yolo = gr.Button("1. Detect Objects", variant="secondary")

                    crop_selector = gr.Dropdown(
                        label="2. Select Detected Object", choices=[], interactive=True
                    )
                    category_dd3 = gr.Dropdown(
                        choices=CIFAR_CLASSES,
                        value="all",
                        label="Filter Candidate Class",
                    )
                    top_k_slider3 = gr.Slider(
                        minimum=1, maximum=12, value=4, step=1, label="Top Results"
                    )
                    btn_search_crop = gr.Button(
                        "3. Search with Selected Object", variant="primary"
                    )

                with gr.Column(scale=2):
                    with gr.Row():
                        annotated_display = gr.Image(
                            type="pil", label="YOLO Scene Detections"
                        )
                        crop_display = gr.Image(type="pil", label="Active Crop Preview")
                    yolo_gallery = gr.Gallery(
                        label="Retrieved Visual Matches", columns=4, height="auto"
                    )

            # Step 1: Detect objects and populate dropdown + state
            btn_run_yolo.click(
                fn=process_scene_detections,
                inputs=[yolo_input],
                outputs=[annotated_display, crop_selector, detected_crops_state],
            )

            # Step 2: Changing dropdown updates crop preview and triggers search
            crop_selector.change(
                fn=query_selected_crop,
                inputs=[
                    crop_selector,
                    detected_crops_state,
                    category_dd3,
                    top_k_slider3,
                ],
                outputs=[crop_display, yolo_gallery],
            )

            # Step 3: Explicit search button trigger
            btn_search_crop.click(
                fn=query_selected_crop,
                inputs=[
                    crop_selector,
                    detected_crops_state,
                    category_dd3,
                    top_k_slider3,
                ],
                outputs=[crop_display, yolo_gallery],
            )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
