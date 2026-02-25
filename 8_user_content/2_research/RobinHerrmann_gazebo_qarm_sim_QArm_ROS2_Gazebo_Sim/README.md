# gazebo_qarm_sim (Quanser QArm, ROS 2 + Gazebo)

## Overview
`gazebo_qarm_sim` is a ROS 2 package that simulates the **Quanser QArm** in **Gazebo**, with a modeled arm and environment intended to support reinforcement learning through a Gym-inspired interface (`QArmEnv`).  
As a research foundation, it provides a modern, ROS 2-native simulation workflow (URDF/XACRO, `ros2_control`, Gazebo integration) where policies and controllers can be iterated safely and repeatably before moving to hardware.

---

## How the Quanser Community Can Use This (research-oriented)
- **RL prototyping with a realistic robot target:** develop and debug training loops against `QArmEnv` before investing time on hardware access and safety setup.
- **Sim-to-real preparation workflow:** use simulation to validate action spaces, termination conditions, and safety checks, then plan a measured transition to QArm hardware (a clean step for research teams and graduate projects).
- **Reproducible baselines for manipulation-style tasks:** use the same simulation and environment definition to compare algorithms (reward shaping choices, exploration strategies, reset logic) under controlled conditions.
- **Controller and middleware research in ROS 2:** evaluate how different control strategies behave through the ROS 2 control stack (`ros2_control`), including timing, command interfaces, and stability under realistic actuation constraints.

---

## Experimental Setup
- **Target platform:** Quanser QArm (simulated)
- **OS:** Ubuntu 22.04
- **ROS 2:** Humble Hawksbill
- **Simulator:** Gazebo 11
- **Control:** `ros2_control` (latest compatible), `gazebo_ros_pkgs` (latest compatible)
- **Model description:** XACRO (latest compatible)

---

## Stack / Tags
`ROS 2`, `Humble`, `Gazebo`, `ros2_control`, `URDF/XACRO`, `Reinforcement Learning`, `Gym-style Env`, `QArm`

---

## Links
* **GitHub Repository:** 
https://github.com/RobinHerrmann/gazebo_qarm_sim

---

## Authors
Robin Herrmann
