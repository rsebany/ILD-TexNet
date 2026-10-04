"""ILD-TexNet: compact texture network for interstitial lung disease (ILD)
pattern classification from 32x32 high-resolution CT texture patches.

This package ships only the proposed architecture, inspection utilities, and
pretrained-weight loading at the call site. Training, evaluation, and the
patient-disjoint leakage benchmark are not included in this repository.
"""

__version__ = "1.0.0"

from ildexnet.models.ildexnet import ILDTexNet  # noqa: E402,F401

__all__ = ["ILDTexNet", "__version__"]