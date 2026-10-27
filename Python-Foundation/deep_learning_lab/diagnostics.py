import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# 1. Device and Model Reconstruction
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DeepCNN(nn.Module):
    def __init__(self):
        super(DeepCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.drop1 = nn.Dropout2d(0.25)

        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.conv4 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.drop2 = nn.Dropout2d(0.25)

        self.fc1 = nn.Linear(64 * 7 * 7, 256)
        self.bn_fc = nn.BatchNorm1d(256)
        self.drop3 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.bn2(self.conv2(x)))
        x = self.pool1(x)
        x = self.drop1(x)

        x = self.relu(self.bn3(self.conv3(x)))
        x = self.relu(self.bn4(self.conv4(x)))
        x = self.pool2(x)
        x = self.drop2(x)

        x = x.view(x.size(0), -1)
        x = self.relu(self.bn_fc(self.fc1(x)))
        x = self.drop3(x)
        return self.fc2(x)


model = DeepCNN().to(device)
model.load_state_dict(
    torch.load("mnist_deep_cnn.pth", map_location=device, weights_only=True)
)
model.eval()

# 2. Load Test Dataset
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
)
test_data = datasets.MNIST(
    root="./data", train=False, download=True, transform=transform
)
test_loader = DataLoader(test_data, batch_size=1000, shuffle=False)

# 3. Collect Predictions & Track Errors
confusion_matrix = torch.zeros(10, 10, dtype=torch.int64)
misclassified_samples = []  # Stores (image, true_label, pred_label, confidence)

with torch.no_grad():
    for images, labels in test_loader:
        images_dev = images.to(device)
        outputs = model(images_dev)
        probs = torch.softmax(outputs, dim=1)
        confs, preds = torch.max(probs, dim=1)

        preds_cpu = preds.cpu()
        confs_cpu = confs.cpu()

        # Update confusion matrix
        for t, p in zip(labels, preds_cpu):
            confusion_matrix[t.long(), p.long()] += 1

        # Identify incorrect classifications
        incorrect_mask = preds_cpu != labels
        if incorrect_mask.any():
            bad_indices = torch.where(incorrect_mask)[0]
            for idx in bad_indices:
                misclassified_samples.append(
                    (
                        images[idx],
                        labels[idx].item(),
                        preds_cpu[idx].item(),
                        confs_cpu[idx].item(),
                    )
                )

print(f"Total test samples: 10,000")
print(f"Total misclassified: {len(misclassified_samples)}")

# 4. Plot & Save Confusion Matrix
fig, ax = plt.subplots(figsize=(8, 7))
cax = ax.matshow(confusion_matrix.numpy(), cmap="Blues")
fig.colorbar(cax)

for i in range(10):
    for j in range(10):
        val = confusion_matrix[i, j].item()
        ax.text(
            j,
            i,
            str(val),
            va="center",
            ha="center",
            color="white" if val > 500 else "black",
            fontsize=9,
        )

ax.set_xticks(range(10))
ax.set_yticks(range(10))
ax.set_xlabel("Predicted Label", fontweight="bold")
ax.set_ylabel("True Label", fontweight="bold")
ax.set_title("MNIST Confusion Matrix", pad=20, fontweight="bold")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
plt.close()
print("Saved 'confusion_matrix.png'")

# 5. Plot & Save Top Misclassified Examples
fig, axes = plt.subplots(2, 5, figsize=(13, 6))
fig.suptitle(
    "Sample Misclassified Digits (True vs Predicted)", fontsize=14, fontweight="bold"
)

for i, ax in enumerate(axes.flat):
    if i < len(misclassified_samples):
        img, true_lbl, pred_lbl, conf = misclassified_samples[i]

        # Undo normalization for visualization
        unnorm_img = img * 0.3081 + 0.1307
        ax.imshow(unnorm_img.squeeze().numpy(), cmap="gray")
        ax.set_title(
            f"True: {true_lbl} | Pred: {pred_lbl}\nConf: {conf * 100:.1f}%", fontsize=10
        )
    ax.axis("off")

plt.tight_layout()
plt.savefig("misclassified_samples.png", dpi=150)
plt.close()
print("Saved 'misclassified_samples.png'")
