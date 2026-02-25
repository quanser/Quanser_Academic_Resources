# MPC- Quanser QUBE-Servo 2 Inverted Pendulum

## Overview
Simulation + real-hardware control code for the **Quanser QUBE-Servo 2 inverted pendulum**, based on Sam Farkhooi’s thesis **“Embedded Model Predictive Control of the Furuta Pendulum.”**  
The control flow is simple: **energy-based swing-up → MPC stabilization with constraints**, designed for real-time execution on an embedded target.

---

## How the Quanser Community Can Use This
- Teach an end-to-end lab: **swing-up → constrained MPC stabilization** on QUBE-Servo 2.
- Use as a **research baseline** for embedded MPC: vary horizons/constraints/sample time and report stability/latency tradeoffs.
- Benchmark against alternatives (e.g., **LQR** or other nonlinear controllers) on the same hardware workflow.
- Reuse the embedded pattern (ESP32 + real-time QP) for other Quanser plants where **constraints + timing** drive the design.

---

## Experimental Setup
- **Plant:** Quanser QUBE-Servo 2 inverted pendulum
- **Simulation:** Python prototyping (CVXPY) in the thesis
- **Embedded control:** MPC in **C++ on ESP32** (PlatformIO), interfacing to the QUBE via **QFLEX 2**

---

## Stack / Tags
`Python`, `C++`, `Embedded MPC`, `QP solver`, `Swing-up`, `Quanser QUBE-Servo 2`

---

## Links
- **GitHub Repository:** 
https://github.com/samfarkhooi/MPC-Furuta-Pendulum
- **Thesis Record:** 
https://uu.diva-portal.org/smash/record.jsf?pid=diva2:1983976
- **Thesis PDF:** 
https://www.diva-portal.org/smash/get/diva2:1983976/FULLTEXT02.pdf

---

## Authors
Sam Farkhooi