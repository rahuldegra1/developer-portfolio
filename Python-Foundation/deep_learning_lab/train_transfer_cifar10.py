import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# 1. Hardware Configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Fine-tuning ResNet-18 on: {device}")

# 2. Pipeline with ImageNet Normalization and Upscaling
# ResNet expects ImageNet stats and larger spatial dimensions
transform_train = transforms.Compose(
    [
        transforms.Resize(128),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

transform_test = transforms.Compose(
    [
        transforms.Resize(128),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

train_data = datasets.CIFAR10(
    root="./data_cifar", train=True, download=False, transform=transform_train
)
test_data = datasets.CIFAR10(
    root="./data_cifar", train=False, download=False, transform=transform_test
)

train_loader = DataLoader(train_data, batch_size=128, shuffle=True, pin_memory=True)
test_loader = DataLoader(test_data, batch_size=256, shuffle=False)

# 3. Load Pretrained Backbone & Modify Classifier Head
weights = models.ResNet18_Weights.DEFAULT
model = models.resnet18(weights=weights)

# Replace the final 1000-class layer with a 10-class output
in_features = model.fc.in_features
model.fc = nn.Linear(in_features, 10)
model = model.to(device)

# 4. Optimization Setup
# A smaller learning rate is used so we don't destroy pretrained weights
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-3)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=5)

# 5. Fine-Tuning Loop (5 Epochs)
EPOCHS = 5
print(f"Starting {EPOCHS}-epoch fine-tuning run...\n")

for epoch in range(1, EPOCHS + 1):
    model.train()
    running_loss = 0.0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    scheduler.step()

    # Evaluation
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()

    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100.0 * correct / total
    print(
        f"Epoch [{epoch}/{EPOCHS}] | Train Loss: {epoch_loss:.4f} | Test Acc: {epoch_acc:.2f}%"
    )

torch.save(model.state_dict(), "resnet18_cifar10.pth")
print("\nModel saved to 'resnet18_cifar10.pth'")
