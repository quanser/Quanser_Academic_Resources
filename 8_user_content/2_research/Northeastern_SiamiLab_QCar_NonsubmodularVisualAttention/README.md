# Non-submodular Visual Attention for Robot Navigation (QCar)

![Non-submodular Visual Attention Diagram](https://raw.githubusercontent.com/SiamiLab/NonsubmodularVisualAttention/qlab/docs/media/diagram.jpeg)
<!-- Image source: SiamiLab/NonsubmodularVisualAttention repository (branch: qlab). -->

## Overview

Visual–Inertial Navigation (VIN/VIO) estimates a robot/car pose using:

- **IMU** (fast, but drifts over time)
- **camera features** (correct drift, but expensive)

In each frame the camera may detect many features. Tracking and optimizing with all of them can be too slow for real-time. The key question is:

> How can we select only **κ “best” features per frame** so VIN stays accurate but runs fast, especially if we know the robot’s near-future motion (anticipation)?

The catch is that the MSE-based scoring objective is **non-submodular**, so classic greedy guarantees do not directly apply.

---

## How Quanser Users Can Use This Work

- Use the **Cancer-Ribbon QCar dataset (EuRoC format)** to benchmark VIO pipelines with motion-capture ground truth.
- Use the provided attention/selection methods to study the tradeoff between **runtime vs accuracy** by tuning **κ**.
- Reproduce **control-aware anticipation** experiments (predict motion over a horizon) and compare against non-anticipation baselines.
- Extend the dataset/experiments to evaluate robustness across turns, low texture, or occlusions, and build toward **multimodal fusion** (camera + IMU + wheel/control).

---

## Experimental Setup

- **Platform:** QCar1
- **Sensors:** Stereo camera + IMU (external stereo camera used in the experiments)
- **Ground truth:** Overhead motion capture (Motive/OptiTrack)
- **Format:** EuRoC-compatible dataset and ROS bag

---

## Stack

**Tags:** `QCar` `ROS` `VIO` `VINS-Mono` `Ceres` `C++` `Python` `Docker`

---

## Links

- **GitHub Repository:**
  https://github.com/SiamiLab/NonsubmodularVisualAttention?tab=readme-ov-file

- **Dataset (IEEE DataPort):**
  https://ieee-dataport.org/documents/visual-inertial-navigation-cancer-ribbon-dataset

- **Paper (arXiv PDF):**
  https://arxiv.org/pdf/2510.00942

---

## Author Preferred Contact

For questions or discussion, please use **[GitHub Issues](https://github.com/SiamiLab/NonsubmodularVisualAttention/issues)** on the project repository. For direct contact, the preferred email is **[behzad.k@northeastern.edu](mailto:behzad.k@northeastern.edu)**.

---

## Authors

Reza Vafaee · Kian Behzad · Milad Siami · Luca Carlone · Ali Jadbabaie
