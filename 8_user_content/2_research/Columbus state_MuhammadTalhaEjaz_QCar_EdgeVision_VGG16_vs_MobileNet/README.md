# Self-Driving-Car-Using-Deep-Learning-Quanser-QCar


## Overview

This work evaluates how well **VGG16** (heavier) versus **MobileNet** (lightweight) can support camera-based perception for a small-scale self-driving platform under **edge-compute constraints** on **Quanser QCar**.

The core question is: **can we keep vision accuracy acceptable while making inference practical on embedded hardware?** The approach relies on **transfer learning** (pretrained weights) and an end-to-end workflow from data collection to deployment-oriented evaluation.

---

## How the Quanser Community Can Use This

- **Start immediately with the included dataset** (no new data collection required).
- Use it as a **teaching lab on edge limits**: train one **light** model and one **heavier** model on the same data, then compare **speed**, **smooth real-time behavior**, and **accuracy**.
- Turn it into a **bottleneck exercise**: measure what slows things down first (image capture, preprocessing, model runtime), make one small change, and re-test.
- Reuse the repo as a **student project template**: keep the dataset and labels, change only one variable (model choice, image size, frame rate), and report the impact with the same test method.

---

## Experimental Setup

- **Platform:** QCar 1
---

## Stack / Tags

**Tags:** `QCar` `Edge AI` `CNN` `MobileNet` `VGG16` `Transfer Learning` `Python` `TFLite`

---

## Links

- **GitHub Repository:**  
  https://github.com/talhaejazh/Self-Driving-Car-Using-Deep-Learning-Quanser-Qcar-?tab=readme-ov-file

- **Paper (IEEE Xplore):**  
  https://ieeexplore.ieee.org/document/10649882

---

## Authors

Muhammad Talha Ejaz
