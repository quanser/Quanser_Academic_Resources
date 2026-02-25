# Robotique RL: QArm Reinforcement Learning

## Overview
This is a sim-to-real RL control workflow for the Quanser QArm (4-DOF), using QLabs (Virtual QArm) as the digital twin for training and evaluation, then deploying to the real hardware.

It trains a **TD3 reinforcement learning agent** to reach **Cartesian target positions** in QLabs, then applies the same control pipeline to the **real QArm hardware**, with **MATLAB/Simulink** as the main training and control stack and optional perception via **RealSense D415 + YOLO** streamed into Simulink over **UDP**.

---

## How the Quanser Community Can Use This
- A practical **sim-to-real workflow** for QArm reaching, using **QLabs (Virtual QArm)** as the digital twin for fast iteration before hardware tests.
- A foundation for **research extensions**: change rewards, observations/actions, constraints, or training settings and study what improves transfer and robustness.
- A baseline for **comparative studies** across RL and classical control (PID/LQR/MPC) using shared metrics like success rate, time-to-target, and tracking error.
- A testbed for **sim-to-real effects** such as noise, delay, and randomization, then validation on the real arm (Robotics, Control Systems, Mechatronics).
- An optional **vision-in-the-loop** path via RealSense + YOLO into Simulink (UDP) for studying partial observability and latency (Computer Vision, Embedded AI).
- A reusable course/capstone module spanning **Reinforcement Learning**, **Robotics/Manipulation**, **Controls**, and **Systems Engineering**.

---

## Experimental Setup
- **Target platform:** QArm
- **Simulation:** Quanser QLabs (Virtual QArm)
- **Algorithm:** TD3 (MATLAB Reinforcement Learning Toolbox)
- **Software:** QUARC + Simulink
- **Vision:** Intel RealSense D415 + YOLO (Python), UDP stream to Simulink

## Stack / Tags
`QLabs`, `Simulink`, `Reinforcement Learning Toolbox`, `TD3`, `QArm`, `QUARC`, `Python`, `ultralytics`, `pyrealsense2`, `YOLO`,

---

## Links
- **GitHub Repository:** 
https://github.com/Heartpray3/qarm-robotic-RL
- **Report:** 
https://github.com/Heartpray3/Quanser-QArm-RL/blob/main/docs/Project_RL_S7.pdf

---

## Authors
Ely Cheikh Abass
