# QArm Fruit Sorting: Classical Vision and Kinematics Behind a Simulink Facade

## Overview
This Applied Robotics coursework project uses the QArm and its built in Intel RealSense D415 camera to sort strawberries, bananas, and tomatoes into three baskets. 

The algorithms for kinematics, HSV fruit detection, trajectory planning, FSM control, and calibration are implemented in Python. A thin Simulink layer calls the Python functions within MATLAB.

The project uses classical robotics and computer vision methods throughout, with autonomous, teleoperation, and optional voice control modes.

---

## How the Quanser Community Can Use This
- As a course module or lab unit: suitable as an Applied Robotics capstone or as a standalone unit on kinematics, classical vision, calibration, or state-machine control. Its pieces map onto a wide range of curricula, from robotics and mechatronics to ECE, mechanical, computer, and electrical engineering.
- An offline-testable reference for analytical plus Newton-Raphson inverse kinematics on the QArm.
- A fully explainable classical alternative (HSV plus contour geometry) to a learned fruit classifier.
---

## Experimental Setup
- **Target platform:**QArm with its built in Intel RealSense D415 camera.
- **Software:** Quanser SDK (HIL, Video3D, Keyboard), Python 3.13, MATLAB/Simulink, OpenCV, Vosk
- **Bridge:** MATLAB `pyenv`, in-process (single address space, no QUARC)
- **Communication:** Quanser HIL board I/O over USB

---

## Stack / Tags
`Python`, `MATLAB/Simulink`, `OpenCV`, `Inverse Kinematics`, `Classical CV`, `Finite State Machine`, `Hand-Eye Calibration`, `Voice Control`, `QArm`, `Quanser SDK`

---

## Links
- **GitHub Repository:**  
https://github.com/PieroJF/Robot-qarm-ruit-sorting

---

## Authors
Piero Flores, Zihen Huang, Ran Zhang, Yichang Chao  
Applied Robotics (04 39984), University of Birmingham