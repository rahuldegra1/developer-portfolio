import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 1. The Data (NumPy Arrays)
# X (Features) must be a 2D array, which is why we use .reshape(-1, 1)
# y (Target) is just a standard 1D array
hours_studied = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(-1, 1)
marks_obtained = np.array([14, 25, 38, 52, 65, 76, 88, 95])

# 2. Initialize the Model
model = LinearRegression()

# 3. Training the Model (Fit)
# This is where the AI actually "learns" the relationship between hours and marks
print("Training the model...")
model.fit(hours_studied, marks_obtained)

# 4. Making a Prediction (Predict)
# Let's ask the model what score a student will get if they study for 7.5 hours
test_hours = np.array([7.5]).reshape(-1, 1)
predicted_score = model.predict(test_hours)

print(
    f"If a student studies for 7.5 hours, the model predicts a score of: {predicted_score[0]:.2f}"
)

# 5. Visualizing the AI's logic
plt.scatter(hours_studied, marks_obtained, color="blue", label="Actual Data")
plt.plot(
    hours_studied, model.predict(hours_studied), color="red", label="AI Prediction Line"
)
plt.title("Student Marks Predictor")
plt.xlabel("Hours Studied")
plt.ylabel("Marks Obtained")
plt.legend()
plt.show()
