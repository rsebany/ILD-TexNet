<div align="center">

# ILD-TexNet

**A compact multi-scale texture network for six-class ILD pattern classification on 32x32 HRCT patches**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-ee4c2c)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green)](https://github.com/rsebany/ILD-TexNet/releases/tag/v1.0.0)

</div>

ILD-TexNet is a multi-scale texture network for interstitial lung disease (ILD) pattern classification on high-resolution CT patches. ~0.25M parameters, trained from scratch, no pretraining. This repository releases the architecture, the inspection utilities, and the pretrained weights.

| Component | Role |
|-----------|------|
| Multi-scale dilated stem | Parallel 3x3 convolutions (dilations 1, 2, 3) |
| Dense SE-MBConv stages | DenseNet-style reuse with MobileNetV3-style inverted residuals + squeeze-excitation |
| Attention pooling | Learned spatial weighting before the classifier |

## Install

```bash
pip install -e .   # or: pip install -r requirements.txt
```

Requires Python >= 3.9 and PyTorch >= 2.0.

## Usage

Build and inspect the model (layer table, parameters, MACs, latency, forward sanity check):

```bash
python main.py
# or, after install: ildexnet [--device cuda --json report.json]
```

Pretrained weights (trained from scratch on MedGIFT HRCT patches): [ILDTexNet.pth](https://github.com/rsebany/ILD-TexNet/releases/download/v1.0.0/ILDTexNet.pth)

The released `ILDTexNet.pth` is a checkpoint that also records the run's provenance
(`state_dict`, `arch_kwargs`, `class_names`, `protocol`, `seed`, `fold`,
`val_macro_f1`, `epochs_run`). Load the weights from the `state_dict` entry:

```python
import torch
from ildexnet import ILDTexNet

ckpt = torch.load("ILDTexNet.pth", map_location="cpu", weights_only=False)
print(ckpt["protocol"], ckpt["seed"], ckpt["fold"])  # e.g. patient 42 2

model = ILDTexNet(**ckpt["arch_kwargs"])
model.load_state_dict(ckpt["state_dict"], strict=True)
model.eval()

patch = torch.randn(1, 1, 32, 32)  # (batch, channel, height, width)
with torch.no_grad():
    logits = model(patch)
```

Architecture flags (`--stem-ch`, `--growth`, `--layers`, `--no-multiscale`, `--block bottleneck`, `--no-attn-pool`, ...) mirror `ILDEXNET_*` environment variables in `ildexnet/config.py`.

## Layout

```
ildexnet/
  models/ildexnet.py    # ILDTexNet module
  models/components.py  # stem, blocks, attention pool
  cli.py                # command-line interface
  complexity.py         # profiling helpers
  config.py             # defaults (enabled via ILDEXNET_* env vars)
tests/
  test_ildexnet.py      # shape/backward, ablation controls, complexity
```

## Dataset and scope

Dataset used: **MedGIFT**, the public ILD database of [Depeursinge et al. (2012)](https://doi.org/10.1016/j.compmedimag.2011.07.003) · [Google Scholar](https://scholar.google.com/scholar?q=%22Building+a+reference+multimedia+database+for+interstitial+lung+diseases%22). MedGIFT is a third-party resource distributed by its owners (University Hospitals of Geneva) and is not redistributed here.

This repository ships the **ILD-TexNet architecture**, inspection utilities (parameter count, MACs, latency), unit tests, and the pretrained weights. It does **not** include patch extraction, the three-level splitting protocol, the automated split-overlap checks, the seven baseline implementations, or the benchmark scripts; the protocol is specified by procedure in the manuscript rather than shipped as assignments.

## Tests

```bash
pip install pytest
pytest -q
```

## License

MIT, see [LICENSE](LICENSE).