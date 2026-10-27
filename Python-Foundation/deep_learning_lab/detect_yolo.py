import torch
import cv2
from PIL import Image
from ultralytics import YOLO

# 1. Device Verification
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Executing YOLO detection on: {device.upper()}")

# 2. Load Pretrained YOLO11 Nano model (weights auto-download on first run)
model = YOLO("yolo11n.pt")

# 3. Target Image
img_path = "download.jpg"  # Uses your sports car photo from earlier

# 4. Run Detection with CUDA Acceleration
# conf=0.3 filters weak predictions; iou=0.5 sets the NMS suppression threshold
results = model.predict(
    source=img_path, device=device, conf=0.3, iou=0.5, save=False, verbose=False
)[0]

# 5. Parse Raw Detection Tensors
print("\n" + "=" * 55)
print(f" DETECTED OBJECTS ({len(results.boxes)} instances found)")
print("=" * 55)

for idx, box in enumerate(results.boxes):
    class_id = int(box.cls.item())
    class_name = model.names[class_id]
    confidence = box.conf.item() * 100

    # Bounding box coordinates: [x_min, y_min, x_max, y_max]
    coords = box.xyxy[0].cpu().tolist()
    x1, y1, x2, y2 = [round(c, 1) for c in coords]

    print(
        f"[{idx + 1}] Class: {class_name:<12} | Conf: {confidence:5.2f}% | Box: [{x1}, {y1}, {x2}, {y2}]"
    )

print("=" * 55)

# 6. Render Bounding Boxes & Save Output
annotated_frame = results.plot()  # Returns BGR numpy array with drawn boxes and labels
output_path = "yolo_detection_result.jpg"
cv2.imwrite(output_path, annotated_frame)
print(f"Annotated visualization saved to '{output_path}'.")
