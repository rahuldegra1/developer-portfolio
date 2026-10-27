import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 1. Device and Model Initialization
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = [
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


def load_trained_resnet(weights_path="resnet18_cifar10.pth"):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 10)
    model.load_state_dict(
        torch.load(weights_path, map_location=device, weights_only=True)
    )
    model.to(device)
    model.eval()
    return model


model = load_trained_resnet()


# 2. Grad-CAM Hook Hooking the Final Convolutional Layer (layer4)
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        target_layer.register_forward_hook(self._save_activations)
        target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, input, output):
        self.activations = output

    def _save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate(self, input_tensor, class_idx=None):
        self.model.zero_grad()
        logits = self.model(input_tensor)

        if class_idx is None:
            class_idx = torch.argmax(logits, dim=1).item()

        # Target the logit of the winning class
        score = logits[0, class_idx]
        score.backward()

        # Global average pool the gradients over spatial dimensions (H, W)
        pooled_gradients = torch.mean(self.gradients, dim=[2, 3], keepdim=True)

        # Weight the activation maps
        cam = torch.sum(pooled_gradients * self.activations, dim=1, keepdim=True)
        cam = F.relu(cam)

        # Normalize heatmap to [0, 1]
        cam = cam - cam.min()
        if cam.max() > 0:
            cam = cam / cam.max()

        return cam.squeeze().cpu().detach().numpy(), class_idx, logits


# 3. Image Preprocessing
img_path = "download.jpg"  # Or your uploaded image path
raw_image = Image.open(img_path).convert("RGB")

preprocess = transforms.Compose(
    [
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

input_tensor = preprocess(raw_image).unsqueeze(0).to(device)

# 4. Generate Heatmap
grad_cam = GradCAM(model, target_layer=model.layer4[-1])
heatmap, pred_idx, logits = grad_cam.generate(input_tensor)

probs = torch.softmax(logits, dim=1)[0]
confidence = probs[pred_idx].item() * 100
predicted_label = CLASS_NAMES[pred_idx]

# 5. Overlay Heatmap onto Original Image
resized_heatmap = Image.fromarray(np.uint8(255 * heatmap)).resize(
    raw_image.size, Image.Resampling.BILINEAR
)
heatmap_np = np.array(resized_heatmap) / 255.0

colormap = plt.get_cmap("jet")
colored_heatmap = colormap(heatmap_np)[:, :, :3]  # Strip alpha

raw_image_np = np.array(raw_image) / 255.0
overlay = 0.5 * colored_heatmap + 0.5 * raw_image_np
overlay = np.clip(overlay, 0, 1)

# 6. Save Visualization Comparison
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle(
    f"Prediction: {predicted_label.upper()} ({confidence:.2f}% confidence)",
    fontsize=14,
    fontweight="bold",
)

axes[0].imshow(raw_image)
axes[0].set_title("Input Image")
axes[0].axis("off")

axes[1].imshow(heatmap_np, cmap="jet")
axes[1].set_title("Class Activation Heatmap")
axes[1].axis("off")

axes[2].imshow(overlay)
axes[2].set_title("Grad-CAM Overlay")
axes[2].axis("off")

plt.tight_layout()
plt.savefig("gradcam_result.png", dpi=150)
plt.close()
print(f"Grad-CAM generated successfully. Saved to 'gradcam_result.png'.")
