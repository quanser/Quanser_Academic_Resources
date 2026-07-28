# Feedback Linearized MPC for QCar

## Overview

This project develops a **sim to real path tracking framework** for the Quanser QCar.

It addresses two practical control challenges: the nonlinear motion of the vehicle and the difficulty of running Model Predictive Control fast enough on real hardware. The proposed controller uses feedback linearization to simplify the vehicle model, then applies MPC while respecting speed and steering limits.

The repository compares Feedback Linearized MPC with Nonlinear MPC and Backstepping in both simulation and physical QCar experiments.

---

## How the Quanser Community Can Use This

- **Reproduce the research results:** use the recorded experimental data and plotting scripts to review the results without requiring the full hardware setup.
- **Create new control experiments:** modify the vehicle model, reference path, controller constraints, prediction horizon, or solver.
- **Benchmark path tracking controllers:** compare Feedback Linearized MPC, Nonlinear MPC, and Backstepping using tracking error, computation time, control effort, and constraint violations.
- **Extend the framework:** integrate alternative state estimators, path planners, adaptive control, robust MPC, or learning based control.
- **Support teaching and capstone projects:** use the repository in Controls, Robotics, Mechatronics, Autonomous Vehicles, or Systems Engineering courses.

---

## Experimental Setup

- **Platform:** Quanser QCar
- **Simulation:** MATLAB and Simulink
- **Control methods:** Feedback Linearized MPC, Nonlinear MPC, and Backstepping
- **State estimation:** Unscented Kalman Filter
- **Sensors and inputs:** Vicon position measurements, IMU data, steering feedback, and encoder measurements
- **Software:** MATLAB, Simulink, and QUARC
- **Experimental data:** MATLAB data files are included in the `Results` folder

---

## Stack / Tags

**Tags:** `QCar` `MATLAB` `Simulink` `QUARC` `Model Predictive Control` `Feedback Linearization` `Nonlinear Control` `Quadratic Programming` `Unscented Kalman Filter` `Path Tracking` `Sim to Real`

---

## Links

- **GitHub Repository:**  
  https://github.com/PreCyseGroup/Feedback-Linearized-MPC-for-self-driving-cars

- **Research Paper:**  
  [A Feedback Linearized Model Predictive Control Strategy for Input Constrained Self Driving Cars](https://arxiv.org/abs/2405.01753)

- **Dataset:**  
  Experimental MATLAB data is included in the repository's `Results` folder.

- **Experiment Video:**  
  https://youtu.be/aeHZKyRfcEo

---

## Authors

C. Tiriolo · W. Lucia
