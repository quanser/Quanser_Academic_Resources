# QBot Standard ROS2 Control and Teleoperation

## Overview

`QBot Standard ROS2 Control and Teleoperation` is a hands-on **ROS2 learning and control package** for the **Quanser QBot Platform** that helps users move from platform bring-up to application-level robotics development. Built to work with the [official `qbot_platform` ros 2 example](https://github.com/quanser/Rubber_Ducky/tree/main/5_research/qbot_platform/ros2), it gives students and researchers clear examples of how to use standard ROS2 topics such as **`/scan`**, **`/joy`**, and **`/cmd_vel`** to build real robot behaviors. The repository brings together a basic ROS2 pub/sub example, a **LiDAR-based obstacle follower** with a simple proportional controller, and a **gamepad teleoperation node** with practical safety features like arm/disarm logic, emergency stop, speed limiting, deadzone filtering, and LED feedback. It provides a clean, accessible starting point for teaching, experimentation, and extension into more advanced work such as **PID, MPC, perception-driven control, and custom autonomy behaviors**. 

## How Quanser Users Can Use This Work

- Use it as a **practical ROS2 starting point** for the QBot Platform, with clear examples that connect core ROS2 communication to real robot behavior.
- Build on the included **LiDAR-based follower** as a foundation for testing **PID, MPC, or other custom control strategies**.
- Use the teleop package as a model for **safe and user-friendly manual control**, including arm/disarm logic, emergency stop, speed limiting, deadzone filtering, and LED feedback.
- Adapt the modules for **teaching, labs, and student projects** that focus on sensing, control, and robot behavior design.
- Extend the packages with **new autonomy logic, or higher-level workflows** as a stepping stone toward more advanced QBot applications.

---

## Experimental Setup

- **Target platform:** QBot Platform
- **Hardware:** LiDAR, Xbox-compatible gamepad, onboard LED strip, NVIDIA Jetson onboard compute
- **Middleware:** ROS2 Humble Hawksbill

---

## Stack

**Tags:** `QBot` `ROS2 Humble` `C++` `LiDAR` `Teleoperation` `Gamepad Control` `Proportional Control` `Standard ROS2 Interfaces` `QUARC` `colcon`

---

## Links

- **GitHub Repository:**  
  https://github.com/Arunmegas93/Advanced-topics-in-ECE

---

## Authors

Arun Megavath  . A. De La Cruz  . Frank Cortez  