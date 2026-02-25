# LNN (Quanser Rotary Flexible Link)

## Overview
An end-to-end, hardware-oriented pipeline for the **Quanser Rotary Flexible Link (RFL)** that lets you **collect data, build training datasets, train a learning-based controller, and deploy/evaluate it on RFL**, with a classic controller baseline for comparison. 

The repo also documents the exact I/O conventions (units, input feature order, and command scaling/clamping) so others can reproduce runs consistently.


---

## How the Quanser Community Can Use This
- **Clone and run** an end-to-end example of a learning-based controller workflow on **RFL** (data → training → evaluation).
- Reuse the **data + dataset-building pipeline** for training *other* models (not just the provided one).
- Use it as a **teaching lab template**: students can run a full **learning-control** pipeline on real RFL hardware and compare it against a **classic LQR** baseline.
- Start from the baseline controller and **benchmark new learning controllers** with the same logging and evaluation scripts.
- Extend for research: change the model, loss, features, or trajectories, then **share repeatable comparisons** with the community.

---

## Experimental Setup
- **Platform:** Quanser Rotary Flexible Link (RFL)
- **Workflow:** hardware logging → dataset creation → model training → evaluation → real-time deployment
- **Runtime target:** real-time execution on RFL (Windows workflow)

---

## Stack / Tags
`Python`, `Learning-based control`, `Benchmarking`, `Real-time hardware`, `Quanser RFL`

---

## Links
- **GitHub Repository:** 
https://github.com/asafsayil93/LNN

---
## Authors
Asaf Sayıl
