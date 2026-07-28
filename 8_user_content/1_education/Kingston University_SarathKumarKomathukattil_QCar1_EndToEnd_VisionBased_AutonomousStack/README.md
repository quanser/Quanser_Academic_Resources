# Deep Learning Perception for the QCar: A Sim-to-Real Self-Driving Stack

## Overview
This MSc dissertation builds an end-to-end perception and control stack for the Quanser QCar, validated first in QLabs simulation and then on real QCar hardware. It combines YOLOv8 detection of traffic lights, stop signs, and no-right-turn signs, ENet lane segmentation, camera-plus-LiDAR obstacle detection, and Pure Pursuit trajectory tracking for waypoint maneuvers.

The **lane segmenter** uses ENet over U-Net, 0.36M parameters versus 31M (about 87x fewer) while slightly exceeding U-Net's accuracy (93.73% vs 93.56% mIoU), a deliberate tradeoff for embedded compute. And **obstacle braking** requires both the depth camera and the LiDAR to independently agree, a conservative rule that reduces false stops. 
The **sim-to-real gap** is measure: YOLOv8 detection drops from 99.50% to 92.87% mAP (about 6.57 points) moving from simulation to hardware, running at 25 FPS in sim and roughly 18-22 FPS on the car.

---

## How the Quanser Community Can Use This
- A reference implementation of a full sim-to-real perception stack on the QCar, going all the way from QLabs to real hardware, where most public QCar examples stop at simpler line-following.
- A worked example of the offboard-compute pattern: a thin client on the car and a laptop GPU running perception and control over TCP/IP, where the round-trip latency directly sets the control-loop timing.
- A practical edge-deployment case study, the ENet-versus-U-Net comparison, showing how to pick a lightweight model for embedded targets without losing accuracy.
- A simple, conservative sensor-fusion pattern for safety: require two independent sensors to agree before braking, a useful contrast point against probabilistic or learned fusion.
- Use it in perception, computer vision, autonomous vehicles, or mechatronics courses and thesis projects that pair classical control (Pure Pursuit, PD steering) with modern deep learning under real compute constraints.

---

## Experimental Setup
- **Platform:** QCar 1 and QLabs virtual QCar 
- **Sensors:** CSI camera, Intel RealSense D435 depth camera, RPLidar A2
- **Perception:** YOLOv8 (traffic lights, stop signs, no-right-turn) and ENet lane segmentation (compared against U-Net offline)
- **Software:** Python, Quasner SDK, with PyTorch, Keras, OpenCV, and Ultralytics YOLO
---

## Stack / Tags
`Python`, `PyTorch`, `YOLOv8`, `ENet`, `U-Net`, `Semantic Segmentation`, `Sensor Fusion`, `LiDAR`, `Intel RealSense`, `Pure Pursuit`, `Sim-to-Real`, `Edge Inference`, `QCar`, `QLabs`

---

## Links
- **GitHub Repository:**  
https://github.com/SarathKumarKomathukattil/deep-learning-perception-system

- **Full Dissertation:**  
https://github.com/SarathKumarKomathukattil/deep-learning-perception-system/blob/main/docs/dissertation.pdf

---

## Author
Sarath Kumar Komathukattil  
ME7743 Dissertation, MSc Mechatronic Systems, Kingston University London  
Supervisor: Dr Olga C Duran