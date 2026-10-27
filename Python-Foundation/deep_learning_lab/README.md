# Deep Learning Lab

A collection of Python experiments covering neural-network training, image classification, model inference, Grad-CAM visualization, ONNX benchmarking, object detection, and visual search.

## Stack

PyTorch, ONNX Runtime, FastAPI, Streamlit, and the packages listed in [`requirements.txt`](requirements.txt).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

This repository keeps downloaded datasets, local indexes, trained weights, and exported model files out of Git. Some experiments require their corresponding data or model artifacts; provide those locally before running the related script.

## Experiments

- Training scripts: `intro_nn.py`, `cnn_mnist.py`, `cnn_mnist_v2.py`, `train_fashion.py`, and `train_cifar10.py`
- Inference and visualization: `predict.py`, `gradcam.py`, `detect_yolo.py`, and `visual_search.py`
- Interfaces and diagnostics: `api.py`, `app_ui.py`, `diagnostics.py`, and `benchmark_onnx.py`

Check each script's inputs and configuration before running it. GPU acceleration depends on a compatible PyTorch/CUDA installation.
