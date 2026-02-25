# A comparison of deep learning-based visual odometry algorithms in challenging scenarios

## Overview

This dataset and accompanying study compare **deep learning-based visual odometry (VO)** methods under **challenging sensing conditions** using data collected on a **Quanser QCar**.

The experiments use a QCar equipped with an **Intel RealSense D435** camera, but **only RGB frames are provided** (1920×1080). **Ground-truth pose** is recorded using an external **Vicon motion capture** system.

**Catch:** The dataset focuses on real-world degradations via **emulated camera/lens failures**, so robustness (not just accuracy on clean data) is the core point of comparison.

---

## How Quanser Users Can Use This Work

- **Benchmark** VO algorithms on a QCar-relevant dataset with motion-capture ground truth for fair comparisons.
- **Stress-test** VO pipelines under degraded sensing (exposure issues, lens contamination/damage) to quantify robustness.
- **Compare runtime vs accuracy** across deep learning VO methods using the short, repeatable sequences.
- **Build labs / assignments** around “robust autonomy under degraded vision” using standardized failure conditions.

---

## Experimental Setup

- **Platform:**  QCar1
- **Sensor data provided:** RGB only
  - **Camera:** Intel RealSense D435
  - **Resolution:** 1920×1080
- **Ground truth:** Vicon motion capture (pose)
- **Emulated failures (per sequence, 5 types):**
  - Camera overexposure
  - Camera underexposure
  - Lens condensation
  - Lens breakage
  - Lens dirt

---

## Stack

**Tags:** `QCar` `Visual Odometry` `Deep Learning` `Benchmarking` `Robust Perception`

---

## Links

- **GitHub Repository:**  
  https://github.com/larocs/modvo?tab=readme-ov-file

- **Dataset (Borealis, DOI: 10.5683/SP3/VIG3FC):**  
  https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/VIG3FC

- **Paper (IEEE Xplore):**  
  https://ieeexplore.ieee.org/document/10553552

---

## Authors

Hudson M. S. Bruno · Ketly M. Cabral · Esther L. Colombini · Sidney N. Givigi
