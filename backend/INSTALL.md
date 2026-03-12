# SecureVision Backend - Installation Guide

## Standard Installation

```bash
# Install most dependencies
pip install -r requirements.txt

# Install PyTorch separately (CPU version for anti-spoofing)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## Why Separate PyTorch Installation?

PyTorch requires a special index URL to install the CPU-only version (much smaller download).
The CPU version is sufficient for facial anti-spoofing detection.

## Alternative: GPU Version (if you have NVIDIA GPU)

```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## Verify Installation

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
```

Should output: `PyTorch version: 2.x.x`

## Troubleshooting

**Error: "Could not find a version that satisfies the requirement"**
- Use the index URL: `--index-url https://download.pytorch.org/whl/cpu`

**Error: "You must install torch"**
- Install PyTorch first before running the backend
- Verify with: `pip list | grep torch`

**Large download size (>2GB)?**
- You're installing the CUDA version. Use `--index-url https://download.pytorch.org/whl/cpu` for CPU-only version (~200MB)
