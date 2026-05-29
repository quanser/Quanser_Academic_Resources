# CNN-Adaptive Line Following with Virtual QBot Platform

## Overview

This repository explores **scene-aware adaptive line following** for the **Quanser QBot Platform** in **QLabs**. A custom CNN classifies the road scene into categories such as straight, curve, crossroad, T-junction, and out-of-route, and those predictions are used to adjust the parameters of a low-level line-following controller. Instead of replacing the controller entirely, the learned model acts as a perception layer that selects more suitable gains and biases for the current scene.

The project is valuable because it connects **deep learning, classical control, and robot deployment** in one workflow. It provides a practical example of how scene understanding can improve a traditional PID-style control loop, while still keeping the architecture readable and modular for teaching, benchmarking, and future extensions. :contentReference[oaicite:1]{index=1}

---

## How Quanser Users Can Use This Work

- Use it as a **QBot learning project** that combines perception and control in one pipeline.
- Compare **scene-aware adaptive control** against a fixed-parameter line-following baseline.
- Reuse the structure to test new **scene classifiers, gain schedules, or controller types**.
- Extend the benchmarking scripts for **ablation studies**, such as CNN vs no-CNN or different junction-handling strategies.
- Use it as a starting point for more advanced work such as **learned gain tuning, reinforcement learning, or richer road-topology estimation**.
- Treat it as a strong **simulation-first baseline** before taking the next step toward **deployment on physical QBot hardware**. 

---

## Experimental Setup

- **Platform:** Virtual QBot Platform
- **Environment:** QLabs
- **Sensor:** Downward-facing CSI camera
- **Control frequency:** 60 Hz
- **CNN inference frequency:** Every 30 frames
---

## Stack

**Tags:** `Digital Twin` `QBot` `QLabs` `Python` `PyTorch` `CNN` `Adaptive Control` `PID` `Computer Vision` `Line Following` `Benchmarking`

---

## Links

- **GitHub Repository:**  
  https://github.com/OanaHuang/AI5_Quanser_QBot_Lab_TeamB

---

## Authors

Viv (`XIAOWEIviv`)  . 云天 (`OanaHuang`)