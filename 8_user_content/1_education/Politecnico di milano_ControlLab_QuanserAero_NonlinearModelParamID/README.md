# Quanser Aero Control Project

## Overview
A Control Lab project that derives a **physics-based nonlinear** model of the **Quanser Aero (2-DOF pitch/yaw)** using a **Lagrangian** approach, then performs **parameter identification** so the nonlinear model matches **real experimental data** (including a separate inner model for **propeller and motor dynamics**). The identified model is **linearized** around operating points (e.g., hover) and used to design and compare controllers for stabilization and tracking, including **PD/PID (with decoupling), LQ/LQ-TV, LMI-based control, and nonlinear MPC**.


---

## How the Quanser Community Can Use This
- Teach **system identification**: replicate the repo’s **physics-based parameter identification** 
- UCompare physics-based system identification vs transfer-function identification (voltage → pitch/yaw, optional cross transfer functions).y.
- Re-run the full pipeline as a repeatable teaching module: **derive nonlinear dynamics → identify parameters → linearize → design controllers → compare performance** on stabilization and tracking tasks.
- Use the controller suite as a menu of lab topics: baseline PD/PID, decoupling, optimal control (LQ/LQ-TV), robust methods (LMI-based), and nonlinear MPC variants.
- Extend with new ID methods/models/controllers and share results with the Quanser community.

---

## Experimental Setup
- **Platform:** Quanser Aero, 2 Degrees of Freedom (2dof helicopter)
- **Modeling:** Nonlinear equations of motion derived using a **Lagrangian approach**
- **Parameter identification:** Physical parameters identified from experimental data to match the nonlinear model to real behavior (e.g., damping, friction, coupling torques, thrust coefficient)

---

## Stack / Tags
`MATLAB`, `Simulink`, `System Identification`, `Lagrangian Modeling`, `Nonlinear Dynamics`, `Linearization`, `PID/PD`, `Fuzzy Control`, `LQ/LQ-TV`, `LMI Control`, `Nonlinear MPC`

## Links
**GitHub Repository:** https://github.com/Lmarzi/QuanserAereo-Control-Lab-Project

---

## Authors
Francesco Berruti; Alessandro Donadi; Fausto Allegrini; Ahmad Labib; Lorenzo Marzi
