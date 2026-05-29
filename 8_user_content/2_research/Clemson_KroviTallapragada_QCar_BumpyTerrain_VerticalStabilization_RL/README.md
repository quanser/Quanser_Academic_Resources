# Road preview based ride comfort control using deep reinforcement learning

![Bump traversal and vertical stabilization](https://raw.githubusercontent.com/ClemsonFA1p1/Krovi_Tallapragada_qcar_stabilization/main/mecc_1.jpg)
<!-- Image source: Krovi_Tallapragada_qcar_stabilization repository (ClemsonFA1p1), branch: main. -->

## Overview

This work targets a practical ride-comfort problem: **reduce vertical bounce (vertical acceleration)** while a vehicle drives over bumps, using what many platforms already have: **speed control + onboard sensing**.

They learn a **continuous commanded-speed policy** with **deep reinforcement learning (DDPG actor–critic)**. The policy maps **[current speed, vertical acceleration, terrain preview] → commanded speed**, encouraging behavior like “slow down early for a bump, then recover.”

**Catch:** the actuator is only **longitudinal speed** (not active suspension), so the reward must balance **comfort vs progress**.

---

## How the Quanser Community Can Use This

   * Use it as a **research baseline** for terrain-aware **speed control** on QCar (single control input, easy to reproduce).
   * Train mostly in **simulation**, then do **short real-car fine-tuning** and validate with the same metrics (smoothness/comfort + progress).
   * Test the **look-ahead idea**: use preview of upcoming bumps to drive smoother behavior, then check if it holds on new tracks.
   * Extend one variable at a time: swap the learning method or add simple **speed/jerk limits**, and compare results apples-to-apples.

---

## Experimental setup

- **Platform:** QCar1
- **Sensors / signals:** encoders (speed), IMU (vertical acceleration), camera-derived bump preview (closeness proxy)
- **Learning:** DDPG actor–critic trained mainly in simulation, with short sim2real fine-tuning
- **Runtime / deployment:** policy runs on a host PC with wireless/TCP-style communication closing the loop to QCar

---

## Stack / Tags

**Tags:** `QCar` `Deep Reinforcement Learning` `DDPG` `Sim2Real` `Ride Comfort` `Preview Control` `MATLAB` `RL Toolbox`

---

## Links

- **GitHub Repository:**
  https://github.com/ClemsonFA1p1/Krovi_Tallapragada_qcar_stabilization?tab=readme-ov-file

- **Paper (ScienceDirect):**
  https://doi.org/10.1016/j.ifacol.2022.11.197
---

## Author Preferred Contact
For questions or discussion, please use **[GitHub Issues](https://github.com/ClemsonFA1p1/Krovi_Tallapragada_qcar_stabilization/issues)** on the project repository.

---
## Authors

Ameya Salvi · John Coleman · Jake Buzhardt · Venkat Krovi · Phanindra Tallapragada
