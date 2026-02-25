# line-following-qbot (QBot Platform)

## Overview

`line-following-qbot` provides two working examples of line following on the QLabs QBot Platform:

1) A classical vision + control approach (thresholding, centroid finding, and a steering mapping).
2) A CNN-based approach (a trained model predicts a movement class from each camera frame).

Both use the same QLabs setup (QBot Platform + Warehouse Simulation) and the same bottom-camera view. The classical pipeline can also save frames, which can be used as training data for the CNN pipeline.

---

## How the Quanser Community Can Use This

- Use this lab to compare classical control vs applied AI on the same robot and environment.
- Use the CNN workflow: collect data, train the model, and run real-time inference to drive the robot.
- Make it a robustness test: change QLabs lighting/exposure, line width, or add visual noise, then record how each method behaves.
- Extend AI/ML: adjust labels, add augmentation, try a different model, or switch from classification to steering-angle regression.
- Implement on QBot Platform to validate on real hardware.

---

## Experimental Setup

* **Target platform:** Quanser Interactive Labs (QLabs) with QBot Platform and the Warehouse Simulation.
* **Sensors / inputs:** bottom camera frames.
* **Compute / host:** Python on a host PC.
  * Classical branch: OpenCV-based image processing and control mapping.
  * CNN branch: PyTorch training and real-time inference plus OpenCV for image handling.
* **Notes:** classical branch supports optional frame saving for dataset collection; CNN branch includes training, deployment, and evaluation scripts.

---

## Stack / Tags

`QLabs`,`Python`, `OpenCV`, `PyTorch`, , `QBot Platform`, `Computer Vision`, `Classical control`, `CNN`

---

## Links

- **GitHub Repository:**  
https://github.com/Azi2333/line-following-qbot
- **Classical control:** 
https://github.com/Azi2333/line-following-qbot/tree/classical-control
- **CNN model:** 
https://github.com/Azi2333/line-following-qbot/tree/cnn-model

---

## Authors

Wang Ziyi (@Azi2333)