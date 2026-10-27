import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# 1. Load Dataset
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# 2. Define Hyperparameters to Track
n_estimators = 50
max_depth = 5

# 3. Start MLflow Run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, random_state=42
    )
    model.fit(X_train, y_train)

    # Predict and evaluate
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")

    # Log metrics
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("f1_score", f1)

    # Log the trained model artifact with trusted types for scikit-learn trees
    mlflow.sklearn.log_model(
        model, "random_forest_model", skops_trusted_types=["sklearn.tree._tree.Tree"]
    )

    print(
        f"Model trained and logged successfully! Accuracy: {acc:.2f}, F1-Score: {f1:.2f}"
    )
