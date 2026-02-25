# QArm Web Dashboard

## Overview
`QArm Web Dashboard` is a **local web-based human-machine interface (HMI)** for controlling and visualizing the **Quanser QArm** using **Python Dash**.  
It combines **manual robot control** (joints, Cartesian moves, LED control) with **live camera visualization** (RGB + depth modes), and adds modular interaction features including **AI-based object detection/localization (YOLOv11)** and **voice control (STT/TTS)**.

---

## How the Quanser Community Can Use This
- A ready-to-run **QArm web dashboard** for hands-on motion tasks (Intro Robotics / Mechatronics labs).
- A reference for **industry-style Quanser projects**: modular code, reliable startup, and end-to-end integration.
- Use **joint + Cartesian control** to explore tracking, limits, and tuning on real hardware (Controls / Control Systems).
- Use the live **RGB/depth** feed with **YOLO** to cover data collection, deployment, and latency vs accuracy tradeoffs (Computer Vision / Embedded AI).
- The full stack (**Dash + QUARC + MySQL + AI**) as a small integration project with logging and repeatable runs (ECE/CS Software Engineering).
- Add **voice commands (STT/TTS)** to discuss safe command design and confirmations (HRI / Human-Machine Interface).

---

## Experimental Setup
- **Target platform:** QArm
- **Host OS:** Windows 10
- **Software:** QUARC
- **Database:** MySQL Server (local, configured)
- **Network:** Internet connection required for initial setup and speech-to-text (STT)
- **Entry point:** `dash_app.py` (started by the launcher process)

---

## Stack / Tags
`Python`, `QUARC`, `MySQL`, `YOLOv11`, `Computer Vision`, `STT/TTS`, `QArm`, `Web HMI`

---

## Links
- **GitHub Repository:**  
https://github.com/DennisLank/BA_Quanser_WebApp

---

## Author
 Dennis Marvin Lank (Ostfalia University of Applied Sciences)
