# neural-networks-for-real-time-CV-control-of-a-Quanser-QArm

## Overview

This is a student lab project (MREN 410 Lab 3) that implements two perception-based behaviors on a Quanser QArm: hand-gesture gripper control and live object-detection visualization on the QArm camera stream using YOLOv8n.


---

## How the Quanser Community Can Use This

* Quick demo that puts camera perception in the control loop on QArm, good for class, lab tours, and outreach.
* Reference for streaming QArm RealSense RGB into OpenCV and running a continuous vision loop in Python.
* Add-on for AI/CV robotics modules: replace the gesture logic, add filtering, and add joint-speed and joint-limit checks. 
* Starting point to go from “detection overlay” to “detection-triggered actions” (for example, start a pick/place step only when a class is detected).

---

## Experimental Setup

* **Target platform:** QArm
* **Sensors / inputs:** QArm RealSense RGB 

---

## Stack / Tags

`QArm`,`Python`, `OpenCV`, `MediaPipe`, `Ultralytics YOLOv8`, `RealSense`

---

## Links

- **GitHub Repository:**  
https://github.com/Noah-Waisbrod/neural-networks-for-real-time-CV-control-of-a-Quanser-QArm

---

## Authors

Noah Waisbrod