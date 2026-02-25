# Illumination-Resilient Lane Detection by Threshold Self-Adjustment Using Newton-Based Extremum Seeking

## Overview

Classical HSV color-threshold lane detection is fast and simple, but it is **fragile to illumination changes** (bright, dim, shadows, indoor lighting). Fixed thresholds that work in one condition can fail in another.

This project makes the thresholds **self-adjusting**: it treats the six HSV bounds as “control variables” and **auto-tunes them online** using **Newton-based Extremum Seeking (ES)** to minimize a lane-detection cost, improving robustness without training a neural network.

---

## How the Quanser Community Can Use This

- **Run a lane-following perception baseline that stays robust across lighting**: compare fixed HSV thresholds vs ES-tuned thresholds under deliberate illumination changes (lights on/off, shadows, exposure shifts).
- **Teach a clean “controls meets vision” lab**: ES/Newton-ES, dithering, and time-scale separation become tangible through a real perception pipeline instead of only controller tuning.
- **Reuse the same pattern beyond lanes**: apply ES to auto-tune threshold-based segmentation for cones, markers, colored objects, or other “simple-but-fragile” perception steps in QCar demos.
- **Build hybrid workflows**: use ES-stabilized masks as a fallback mode or as pseudo-labels for lightweight learning systems when training data is limited.

---

## Experimental Setup

- **Platform:** QCar1

---

## Stack / Tags

**Tags:** `QCar` `MATLAB` `Simulink` `QUARC` `Lane detection` `Extremum seeking` `Adaptive perception`

---

## Links

- **GitHub Repository:**  
  https://github.com/bryantzhou/IEEE-T-ITS-2022

- **Paper (IEEE Xplore):**  
  https://ieeexplore.ieee.org/document/9749177

- **Sample video data (MATLAB format, Google Drive):**  
  https://drive.google.com/drive/folders/1aHT1F-vsleInBYi2nPzVcfSRCEN7BSEg?usp=sharing

---

## Authors

Yujing Zhou · Zejiang Wang · Junmin Wang
