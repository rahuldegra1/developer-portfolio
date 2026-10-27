import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Hardware Acceleration Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Neural Network running on: {device}")

# 2. Prepare Data (Transitioning from scikit-learn to PyTorch Tensors)
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert NumPy arrays to PyTorch Tensors and move to GPU
X_train_tensor = torch.FloatTensor(X_train).to(device)
y_train_tensor = torch.FloatTensor(y_train).view(-1, 1).to(device)
X_test_tensor = torch.FloatTensor(X_test).to(device)
y_test_tensor = torch.FloatTensor(y_test).view(-1, 1).to(device)


# 3. Define the Neural Network Architecture
class DeepBinaryClassifier(nn.Module):
    def __init__(self, input_dim):
        super(DeepBinaryClassifier, self).__init__()
        self.layer1 = nn.Linear(input_dim, 64)  # Hidden Layer 1
        self.relu1 = nn.ReLU()  # Activation Function
        self.layer2 = nn.Linear(64, 32)  # Hidden Layer 2
        self.relu2 = nn.ReLU()  # Activation Function
        self.output_layer = nn.Linear(32, 1)  # Output Layer
        self.sigmoid = nn.Sigmoid()  # Probability Output

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu1(x)
        x = self.layer2(x)
        x = self.relu2(x)
        x = self.output_layer(x)
        return self.sigmoid(x)


model = DeepBinaryClassifier(input_dim=20).to(device)

# 4. Define Loss Function and Optimizer
criterion = nn.BCELoss()  # Binary Cross Entropy Loss
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 5. The Training Loop (The core difference from scikit-learn)
epochs = 100
for epoch in range(epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)

    # Backward pass and optimize (Backpropagation)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

# 6. Evaluation
model.eval()  # Set to evaluation mode
with torch.no_grad():
    predictions = model(X_test_tensor)
    predicted_classes = predictions.round()
    accuracy = (
        predicted_classes.eq(y_test_tensor).sum() / float(y_test_tensor.shape[0])
    ).item()
    print(f"\nFinal Test Accuracy: {accuracy * 100:.2f}%")
