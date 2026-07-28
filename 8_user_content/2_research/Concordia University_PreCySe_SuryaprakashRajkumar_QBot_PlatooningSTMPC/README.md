# Set Theoretic MPC for QBot Platform Platooning

## Overview

This project develops a **real time platooning framework for three QBot Platforms** following the same figure eight path.

It focuses on coordinated multi robot navigation using model predictive control on physical robots. The controller combines precomputed reachable sets with a lightweight online optimization to achieve real time path tracking while respecting wheel speed limits.

The leader follows a figure eight trajectory, while the two followers track delayed versions of the same path. A collision avoidance supervisor continuously adjusts each follower's delay to maintain safe spacing between robots.

---

## How the Quanser Community Can Use This

* **Study multi robot platooning:** use the leader and follower models as a starting point for coordinated QBot experiments.
* **Explore real time predictive control:** examine how offline reachable sets reduce the amount of optimization required during operation.
* **Evaluate safe spacing strategies:** modify the minimum distance, follower delay, wheel speed limits, or collision avoidance logic.
* **Create comparative studies:** compare Set Theoretic MPC with conventional MPC, PID, consensus control, or learning based multi agent control using tracking error, spacing error, computation time, and constraint violations.
* **Extend the framework:** add more robots, alternative reference paths, distributed communication, onboard localization, or different state estimators.
* **Support teaching and capstone projects:** use the repository in Controls, Robotics, Mechatronics, Autonomous Systems, or Multi Agent Systems courses.

---

## Experimental Setup

* **Platform:** Three Quanser QBot Platforms differential drive robots
* **Localization:** Vicon Vero motion capture system
* **Communication:** TCP over a local WiFi network
* **Software:** MATLAB R2022b or later, Simulink, and Quanser QUARC

---

## Stack / Tags

**Tags:** `QBot` `MATLAB` `Simulink` `QUARC` `Set Theoretic MPC` `Multi Robot Systems` `Platooning` `Collision Avoidance` `Vicon` `Trajectory Tracking` `Differential Drive`

---

## Links

* **GitHub Repository:**  
  https://github.com/PreCyseGroup/Platooning_STMPC_QBOT

* **Research Paper:**  
  [A Set Theoretic Control Strategy for a Platoon of Constrained Differential Drive Robots with Inter Vehicle Collision Avoidance](https://doi.org/10.1109/TASE.2026.3656805)

* **Experiment Video:**  
  https://www.youtube.com/watch?v=v7aPkgLL9KI

---

## Authors

Suryaprakash Rajkumar · Cristian Tiriolo · Walter Lucia