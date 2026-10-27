import torch
import torch.nn as nn
from torchvision import datasets, transforms

# 1. Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 2. Re-instantiate the identical model architecture
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(16 * 14 * 14, 10)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = x.view(-1, 16 * 14 * 14)
        return self.fc1(x)


# 3. Load the model and map weights
model = SimpleCNN().to(device)
model.load_state_dict(
    torch.load("mnist_cnn.pth", map_location=device, weights_only=True)
)
model.eval()

# 4. Pull a single sample image from MNIST test data
transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)
test_data = datasets.MNIST(
    root="./data", train=False, download=True, transform=transform
)

sample_image, true_label = test_data[0]  # First test image
input_tensor = sample_image.unsqueeze(0).to(
    device
)  # Add batch dimension: [1, 1, 28, 28]

# 5. Run inference
with torch.no_grad():
    raw_logits = model(input_tensor)
    probabilities = torch.softmax(raw_logits, dim=1)
    predicted_digit = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][predicted_digit].item() * 100

print(f"True Label: {true_label}")
print(f"Predicted Digit: {predicted_digit} ({confidence:.2f}% confidence)")
