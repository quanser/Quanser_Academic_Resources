# Model Predictive Control for the Quanser Aero 2: A Three-Stage Sim-to-Twin Study

## Overview
This Advanced Control coursework project implements a constrained Model Predictive Controller (MPC) for the Quanser Aero 2, a 2-DOF pitch/yaw helicopter rig. The controller is built and validated in three stages of increasing realism: a discrete linear model in plain MATLAB, the same controller in a real-time Simulink loop, and finally against Quanser's nonlinear virtual twin in QLabs, without changing the controller between stages. 

The three stages let you measure how a linear controller degrades against a nonlinear plant: tracking error jumps about 21x from stage 2 to stage 3, which marks where the linear model stops being accurate enough (yaw overshoot from cross-coupling, steady-state offset from unmodelled friction) rather than a failure of the controller.

---

## How the Quanser Community Can Use This
- A ready worked example of MPC on the Aero 2, with all the QP scaffolding (prediction, cost, and constraint matrix builders) that is usually the hardest part to get right, reusable for other linear MIMO plants.
- A three-stage validation template for deploying any controller onto Quanser hardware or virtual twins: linear MATLAB, then real-time Simulink, then the nonlinear QLabs twin, isolating one failure source at a time.
- A starting point for physical deployment on Aero 2.
- A concrete study of the reality gap, with proposed fixes (integral action, online steady-state re-identification) for the coupling and friction effects it exposes.
- Suitable as an advanced controls or MPC teaching lab and for coursework or thesis projects, since each stage maps to a distinct concept: state-space modelling, discretization, QP formulation, constraints, and receding-horizon control.

---

## Experimental Setup
- **Platform:** QLabs Virtual Aero 2 and Aero 2 
- **Software:** MATLAB/Simulink with QUARC
---

## Stack / Tags
`MATLAB`, `Simulink`, `QUARC`, `Model Predictive Control`, `Quadratic Programming`, `Constrained Control`, `LQR`, `Sim-to-Real`, `Aero 2`, `QLabs`

---

## Links
- **GitHub Repository:**
https://github.com/nijatbadalov04-alt/ELE461-MPC-Quanser-Aero2

- **Report:**
https://github.com/nijatbadalov04-alt/ELE461-MPC-Quanser-Aero2/blob/main/docs/ELE461_Advanced_Control_Report.pdf

---

## Author
Nijat Badalov  
ELE461 Advanced Control, University of Sheffield