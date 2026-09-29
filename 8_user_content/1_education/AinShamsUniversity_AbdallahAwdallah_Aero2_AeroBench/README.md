# AeroBench: Controller Comparison in MATLAB (Quanser Aero 2 Model)

## Overview

`AeroBench` brings **nine controller implementations** together on a nonlinear MATLAB model of Quanser Aero 2: classical, adaptive, and gain scheduled PID; LQR; linear MPC; super twisting and fast terminal sliding mode control; a neural controller trained from PID examples; and nearest neighbor regression with LQR feedback.

Shared test scenarios, plots, and metrics give educators a starting point for **teaching control methods from introductory to advanced courses** without building a separate test environment for each controller.

---

## How the Quanser Community Can Use This

- **Introductory control courses:** use PID exercises to teach tuning, overshoot, settling behavior, and control effort.
- **Advanced courses:** compare optimal, adaptive, sliding mode, and learning based control under disturbances, noise, and parameter changes.
- **Course projects:** ask students to modify or add a controller, then compare tracking and motor commands under identical test conditions.
- **Digital twin to hardware:** adapt selected controllers for the [QLabs Aero 2 digital twin][qlabs], then evaluate them on physical Aero 2. These extensions require device interfaces and validation; neither connection is included in AeroBench.

---

## Experimental Setup

- **Platform:** mathematical model of Quanser Aero2 :2 DOF Helicopter
- **Included controllers:** classical, adaptive, and gain scheduled PID; LQR; linear MPC; two sliding mode implementations; a neural controller trained from PID examples; and nearest neighbor regression with LQR feedback.

---

## Stack / Tags

`Aero 2`, `MATLAB`, `Control Education`, `PID`, `LQR`, `MPC`, `Sliding Mode Control`, `Machine Learning`

---

## Links

- **Repository:** [AeroBench source code and documentation][repo].
- **Controllers:** [The nine controller implementations][controllers].
- **Digital twin for extension projects:** [QLabs Virtual Aero 2][qlabs].

---

## Authors

Abdallah Mohamed Awdallah; Sherif A. Hammad; Mohamed Ibrahim Awad; Diaa Emad.

Faculty of Engineering, Ain Shams University, Egypt.

[repo]: https://github.com/aero2-benchmark/aero2-benchmark
[controllers]: https://github.com/aero2-benchmark/aero2-benchmark/tree/main/matlab/controllers
[qlabs]: https://www.quanser.com/products/qlabs-virtual-aero-2/
