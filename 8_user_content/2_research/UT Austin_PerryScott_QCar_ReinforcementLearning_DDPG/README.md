# Autonomous Driving with Reinforcement Learning


## Overview

This repository is a practical baseline for running **reinforcement learning on QCar-scale vehicle control** using **DDPG (Deep Deterministic Policy Gradient)**.

The core idea is to learn a **continuous control policy** (throttle and steering) from recorded driving experience, then evaluate the learned policy as a controller. The codebase implements an actor–critic learner with a replay buffer and target networks, and it supports training from saved experience logs. citeturn6search4

---

## How the Quanser Community Can Use This

- **“RL on real car” starting point:** a concrete repository you can clone and adapt for speed tracking or path-following style learning-based control.
- **Reusable training loop:** DDPG-style actor/critic structure, target networks, and replay-buffer workflow are widely reusable across QCar RL projects.
- **Clear extension surface:** swap rewards, state definitions, or action bounds to move toward safe RL, sim-to-real, or robust control under disturbances.

---

## Experimental setup

- **Platform:** Quanser QCar (scaled autonomous vehicle).
- **Control:** continuous actions consistent with throttle and steering bounds used in the learner.
- **Learning:** DDPG actor–critic with replay buffer, target networks, and offline training from stored experience.

---

## Stack / tags

**Tags:** `QCar` `Reinforcement Learning` `DDPG` `Python` `TensorFlow` `MATLAB`

---

## Links

- **GitHub Repository:** 
https://github.com/perryascott/qcar_RL

---

## Authors

Perry A. Scott · Bryant Zhou
