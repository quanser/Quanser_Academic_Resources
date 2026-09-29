# Cascaded MPC Flight Control (Quanser QDrone 2)

## Overview

This project is a **cascaded Model Predictive Control (MPC) implementation for Quanser QDrone 2**, developed in MATLAB and Simulink. It includes separate controllers for altitude, attitude, and horizontal position, with editable models and controller calculations..

Built on [**Quanser’s DroneStack**](https://github.com/quanser/Quanser_Academic_Resources/tree/dev-windows/5_research/autonomous_vehicles), it connects these controllers to onboard sensors, motor outputs, and ground station mission models. The shared implementation gives researchers a starting point for modifying the control design while reusing the existing sensing, communication, and motor interfaces.

---

## How the Quanser Community Can Use This

- **Compare predictive control with PID:** change one control layer at a time and test the same climb or flight path. Compare tracking error, overshoot, motor commands, and computation time.
- **Explore how far ahead to predict:** change the prediction horizons and tracking versus control effort weights in Setup_QDrone2_MPC.m. Measure the effect on tracking and computation time.
- **Add limits inside the optimizer:** develop and validate a constrained solver using the included matrix helpers as a starting point. Compare limit violations and computation time against the existing solution.
- **Design smoother flight commands:** adapt the mission models to compare abrupt waypoint changes with gradual references along the same route (Controls, Robotics, or Mechatronics projects).

---

## Experimental Setup

- **Platform:** Quanser QDrone 2
- **Software:** MATLAB, Simulink, QUARC, and Control System Toolbox
- **Sensing and outputs:** dual IMU attitude estimation, height sensing, and motor/ESC commands.
---

## Stack / Tags

`QDrone 2`, `MATLAB`, `Simulink`, `QUARC`, `MPC`, `Flight Control`, `Trajectory Tracking`


---

## Links

- **Repository:** [MPC_Drone_quanser][repo]. MATLAB source, Simulink models, and documentation; MIT license listed in the repository.

---

## Author

Carlos Hernán

Tecnológico de Monterrey (ITESM).


[repo]: https://github.com/carlos2219/MPC_Drone_quanser