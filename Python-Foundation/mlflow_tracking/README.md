# MLflow Experiment Tracking

A reproducible Iris-classification experiment that trains a scikit-learn Random Forest and logs its hyperparameters, accuracy, weighted F1 score, and model artifact with MLflow.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install mlflow scikit-learn
python train.py
mlflow ui
```

Open the MLflow UI at `http://127.0.0.1:5000`. Run the training script again to create another tracked experiment run. Local tracking databases and run artifacts are excluded from Git.
