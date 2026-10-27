import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 1. Hardware Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on: {device}")

# 2. Load & Normalize MNIST Dataset (Images of handwritten digits)
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)
train_data = datasets.MNIST(
    root="./data", train=True, download=True, transform=transform
)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)


# 3. Define the CNN Architecture
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # Convolutional Layer: 1 input channel (grayscale), 16 output filters, 3x3 kernel
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        # Pooling Layer: Downsamples the image by half
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        # Fully Connected (Linear) Layer: Maps the flattened 2D data to 10 digit classes
        self.fc1 = nn.Linear(16 * 14 * 14, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(-1, 16 * 14 * 14)  # Flatten the 2D matrices into a 1D vector
        x = self.fc1(x)
        return x


model = SimpleCNN().to(device)


# 4. Define Loss Function and Optimizer
criterion = nn.CrossEntropyLoss()  # Used for multi-class classification
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Training Loop (1 Epoch for a quick test)
print("Starting training...")
for batch_idx, (images, labels) in enumerate(train_loader):
    images, labels = images.to(device), labels.to(device)

    # Forward pass
    outputs = model(images)
    loss = criterion(outputs, labels)

    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if batch_idx % 200 == 0:
        print(f"Batch {batch_idx}/{len(train_loader)} | Loss: {loss.item():.4f}")

print("\nCNN trained successfully for 1 epoch!")
# 6. Evaluate on Unseen Test Data
test_data = datasets.MNIST(
    root="./data", train=False, download=True, transform=transform
)
test_loader = DataLoader(test_data, batch_size=1000, shuffle=False)

model.eval()  # Set model to evaluation mode
correct = 0
total = 0

with torch.no_grad():  # Disable gradient tracking to save VRAM and compute
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_accuracy = 100.0 * correct / total
print(f"Test Accuracy on 10,000 images: {test_accuracy:.2f}%")

# 7. Save Model Weights
torch.save(model.state_dict(), "mnist_cnn.pth")
print("Model state dictionary successfully saved to 'mnist_cnn.pth'")
