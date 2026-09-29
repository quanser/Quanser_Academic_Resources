# Mobile Wi-Fi CSI–Based Object Detection with QCar

![QCar Wi-Fi CSI Object Detection Setup](https://raw.githubusercontent.com/SiamiLab/MobileCSIObjectDetection/main/resources/floor_plan.jpg)
<!-- Image source: MobileCSIObjectDetection repository (SiamiLab). -->

## Overview

This repository shows how two QCars using standard Wi-Fi hardware can perform **non-line-of-sight object detection** with **Channel State Information (CSI)**.

By driving around a closed container and analyzing Wi-Fi reflections, the system classifies whether the box is **empty or filled**, treating QCar as a **mobile RF sensing platform**.

---

## How Quanser Users Can Use This Work

- Start immediately with the **ready-made dataset** to benchmark CSI preprocessing pipelines and machine learning models.
- Test your own **feature extraction or deep learning** methods for RF-based perception using the provided CSI measurements.
- Extend the dataset with **new objects, materials, trajectories, speeds, or environments** to study robustness and generalization.
- Combine CSI with QCar sensors (camera, IMU, odometry, LiDAR) for **multimodal perception and sensor fusion** research.
- Explore research directions in **RF perception**, **privacy-preserving sensing**, and **wireless-aware robotics**.

---

## Experimental Setup

- **Platforms:** Two QCar 1s
  - QCar #1: Wi-Fi transmitter
  - QCar #2: CSI receiver (Raspberry Pi with Nexmon)
- **Motion:** Circular trajectories around a closed box
- **Sensing:** Wi-Fi Channel State Information (CSI)
- **Task:** Classify box as *empty* or *filled*
- **Data:** Publicly available CSI dataset

---
## Stack

**Tags:** `QCar` `WiFi` `CSI` `Nexmon` `RF-Sensing` `MATLAB` `Dataset`

## Links

- **GitHub Repository:**
  https://github.com/SiamiLab/MobileCSIObjectDetection

- **Dataset:**
  https://github.com/SiamiLab/MobileCSIObjectDetection/tree/main/dataset

- **Reference Paper:**
  *Mobile Wi-Fi CSI-Based Object Detection Using Autonomous Robots*
  IEEE PerCom Workshops, 2025
  DOI: 10.1109/PerComWorkshops65533.2025.00116
  https://ieeexplore.ieee.org/document/11038594

---
## Author Preferred Contact

For questions or discussion, please use **[GitHub Issues](https://github.com/SiamiLab/MobileCSIObjectDetection/issues)** on the project repository. For direct contact, the preferred email is **[behzad.k@northeastern.edu](mailto:behzad.k@northeastern.edu)**.

---

## Authors

Kian Behzad · Maral Mordad · Rojin Zandi · Milad Siami