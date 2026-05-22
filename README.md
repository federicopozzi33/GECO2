# GeCo2 - Generalized-Scale Object Counting with Gradual Query Aggregation

> Official repository of **GeCo2**  
> 🏆 **Accepted to AAAI 2026**  
> 📄 Read the paper: [GeCo2 PDF](https://arxiv.org/pdf/2511.08048)

---


## Abstract

Few-shot detection-based counters estimate the number of category instances in an image using only a few test-time exemplars. Existing methods often rely on ad-hoc image upscaling and tiling to detect small, densely packed objects, and they struggle when object sizes vary widely within a single image.  **GeCo2** introduces a generalized-scale dense query map that is gradually aggregated across multiple backbone resolutions. Scale-specific query encoders interact with exemplar appearance and shape prototypes at each feature level and then fuse them into a high-resolution query map for detection. This avoids heuristic upscaling/tiling, improves counting and detection accuracy, and reduces memory and runtime. A lightweight SAM2-based mask refinement further polishes box quality.  On standard few-shot counting/detection benchmarks, GeCo2 achieves strong gains in MAE/RMSE and AP/AP50, while running ~3× faster with a smaller GPU footprint.

https://github.com/user-attachments/assets/8b5f3f06-45f8-439f-9333-b7a747db28a5

## Live Demo
Try the interactive demo on Hugging Face:  
👉 [DEMO HERE](https://huggingface.co/spaces/jerpelhan/GECO2-demo)


## Installation as a dependency

The repository can now be installed directly as a Python package.

Tested installation paths:

- `pip install .`
- `pip install -e .`
- `pip install git+https://github.com/jerpelhan/GECO2.git`

### Core package

```bash
pip install git+https://github.com/jerpelhan/GECO2.git
```

### Optional extras

```bash
# Demo UI dependencies
pip install -e ".[demo]"

# Evaluation helpers (Detectron2 still needs to be installed separately)
pip install -e ".[eval]"
```

### Editable install from source

```bash
pip install -e .
```

### Standard install from source

```bash
pip install .
```

### Build a wheel manually

```bash
python -m pip install --upgrade build
python -m build --wheel
pip install dist/geco2-0.1.0-py3-none-any.whl
```

The optional CUDA extension for deformable attention is built automatically when possible.  
If compilation is not available, installation still succeeds and GECO2 falls back to a slower pure-PyTorch implementation.

### Quick verification

After installation, you can verify that the package is available with:

```bash
python -c "import geco2; print(geco2.__version__)"
```

### macOS note: missing `_lzma`

Some Python builds on macOS are compiled without `lzma` support. In that case, importing heavier optional modules may fail with:

```text
ModuleNotFoundError: No module named '_lzma'
```

This is a Python runtime issue, not a GECO2 packaging issue. If you hit it, reinstall Python with `xz` support enabled. For example, with Homebrew + pyenv:

```bash
brew install xz
export LDFLAGS="-L$(brew --prefix xz)/lib"
export CPPFLAGS="-I$(brew --prefix xz)/include"
pyenv install 3.12.9
pyenv local 3.12.9
```

Then recreate your virtual environment and reinstall GECO2.


## Highlights
<img width="2575" height="912" alt="GECO2_first_image_motivation_neurips-1" src="https://github.com/user-attachments/assets/adf4dcfd-aa17-4cff-9113-8b8a0e37de31" />

- 🔁 **Gradual cross-scale query aggregation** → one high-res dense query map without tiling.  
- 🧩 **Per-scale exemplar interaction** with **appearance** + **shape** prototypes.  
- ⚡ **Fast & memory-efficient** inference.  
- 📈 Strong results on **FSCD147**, **FSCD-LVIS**, and **MCAC** (few-shot & multi-class).


<img width="2097" height="587" alt="Geco2_architevture-1" src="https://github.com/user-attachments/assets/88d27ee8-e84e-409a-a87d-095ca24e8a89" />


## Demo Installation

You can easily install and run the demo using the provided `install.sh` script.

```bash
bash install.sh
```

#### Download Weights

Download the model weights from:

👉 [CNTQG_multitrain_ca44.pth](https://huggingface.co/datasets/jerpelhan/geco2-assets/resolve/main/weights/CNTQG_multitrain_ca44.pth?download=true)

and place the file in the **project root directory**.

#### Launch the Demo

Then run:

```bash
python demo_gradio.py
```
---
<img width="1832" height="2661" alt="GeCoV2Qualitative_segmentation-1" src="https://github.com/user-attachments/assets/8797ada0-e8a7-4e4c-8967-4ebbb365f63f" />

---



## Reproducing Results on FSCD147

This section describes how to reproduce the reported counting and detection results on the **FSCD147** benchmark.

### Prerequisites

Both training and inference require **Detectron2** for evaluation of detection metrics (**AP** / **AP50**).

Please install Detectron2 following the official instructions corresponding to your PyTorch and CUDA versions.

---

### Option 1: Retraining on FSCD147

1. Train the model:

First correct data_path and model_path in train.sh, then run: 
```bash
        bash train.sh
```

2. Evaluate detection performance (AP / AP50):
```bash
        python eval_bboxes.py
```
---

### Option 2: Inference with Official Weights

1. Download official [weights for FSCD GECO2](https://drive.google.com/file/d/1OG6-tTP2Egvx-O5oK6lxPzvQO1LWgHbb/view?usp=sharing)


2. Run evaluation:
```bash
        python eval_bboxes.py
```


    
## Citation

If you find this work useful, please cite:

```bibtex
@inproceedings{pelhan2026generalized,
  title={Generalized-Scale Object Counting with Gradual Query Aggregation},
  author={Pelhan, Jer and Luke{\v{z}}i{\v{c}}, Alan and Kristan, Matej},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={40},
  number={10},
  pages={8314--8321},
  year={2026}
}
```
