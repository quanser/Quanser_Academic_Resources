# QArm Simulator: From-Scratch Kinematics with Webcam Gesture Control

## Overview
This project is a Python simulator of the QArm that you drive by moving your own arm in front of a webcam: a pretrained pose model reads your shoulder, elbow, and wrist, and the on-screen arm mirrors you in real time. You can also drive it manually with keyboard and sliders. The kinematics, the live 3D view, and the gesture pipeline are all built from scratch, with the arm's geometry matched to the published QArm specs.

---

## How the Quanser Community Can Use This
- A ready lecture demo for forward and inverse kinematics: move one joint at a time and show angles-in / position-out, or set a target and watch the arm solve and animate to it.
- A short, readable codebase to hand students as a project base, with clear next steps like adding a gripper, solving the wrist joint, or adding collision checks.
- An accessible first look at pairing computer vision with robotics, showing webcam-based teleoperation without a motion-capture rig.
- A hands-on way to contrast ideal joints with real hardware limits, using the built-in physics toggle.

---

## Experimental Setup
- **Platform:** desktop Python simulation of the QArm (4-DOF geometry matched to the published QArm spec)
- **Perception:** standard webcam plus a pretrained YOLOv8-pose model detecting shoulder, elbow, and wrist
- **Control:** live gesture mirroring, or manual keyboard and slider control
- **Software:** Python 3.8+, NumPy, Matplotlib, OpenCV, Ultralytics (YOLOv8-pose)

---

## Stack / Tags
`Python`, `NumPy`, `Matplotlib`, `OpenCV`, `YOLOv8-pose`, `Forward Kinematics`, `Inverse Kinematics`, `Gesture Control`, `QArm`

---

## Links
- **GitHub Repository:**  
https://github.com/phanghonghao/qarm-robot-simulator

---

## Author
Phang Hong Hao  
Tsinghua University