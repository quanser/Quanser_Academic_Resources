# Mamba-MPC: Learned Dynamics for Predictive Control (Quanser Aero 2)

## Overview

This project uses **Mamba, a neural network trained on experimental data, as the prediction model inside Model Predictive Control (MPC)**. Mamba predicts how Aero 2's pitch and yaw will respond to proposed motor voltages. MPC uses those predictions to choose the commands. **The challenge is making those predictions accurate enough for control and fast enough to use during operation.**

The [researchers][paper] adapted Mamba to predict several future steps in one pass and implemented the controller on a **physical Quanser Aero 2 at 25 Hz**. The repository shares Python notebooks, training data, saved models, and the code connecting PyTorch predictors to a CasADi optimizer. Other Aero 2 users can build on this workflow to compare prediction models, training methods, and controllers.

---

## How the Quanser Community Can Use This

- **Compare predictors on Aero 2:** adapt the included LSTM and Transformer models to the Aero 2 recordings. Match training data and horizons; compare prediction error, tracking, and computation time. The existing hardware experiment uses Mamba only.
- **Study data requirements:** retrain on smaller portions of the recordings or data from your own Aero 2. Test how much data is needed for useful predictions and control.
- **Compare learned and conventional control:** use the same references and operating limits to compare Mamba-MPC with a physics model inside MPC or a PID controller.
- **Improve control timing:** vary the horizon, network size, or solver. Compare tracking with average and worst observed computation time, including missed control deadlines (Machine Learning, System Identification, or Controls projects).
- **Extend to other Quanser plants**: adapt the workflow for QArm joint tracking or inverted pendulum balancing.
---

## Experimental Setup

- **Platform:** Quanser Aero2 :2 DOF Helicopter
- **Inputs and outputs:** two motor voltages; predicted pitch and the sine and cosine of yaw. Pitch and yaw rates also form part of the initial condition.
- **Data collection:** the [paper][preprint] reports 240,000 samples at 100 Hz, downsampled to 25 Hz for model training.
- **Software:** Python, PyTorch, CasADi, Jupyter, and the Quanser Python SDK. The Aero 2 experiment uses an SQP solver.

---

## Stack / Tags

`Aero 2`, `Python`, `PyTorch`, `CasADi`, `Mamba`, `MPC`, `System Identification`, `Learning Based Control`

---

## Links

- **Repository:** [Mamba-MPC][repo]. Source code, notebooks, data, saved models, and results.
- **Paper:** [Mamba Sequence Modeling Meets Model Predictive Control][paper]. IEEE Open Journal of Control Systems, 2026.
- **Open access preprint:** [arXiv:2604.13857][preprint]. Aero 2 setup and experimental results.
- **Hardware video:** [Mamba-MPC reference tracking on Quanser Aero 2][video].

---

## Authors

Michiel Cevaal; Thomas O. de Jong; Mircea Lazar.

**Affiliations:** Tilburg University; Eindhoven University of Technology, The Netherlands.

[repo]: https://github.com/cmichiel/Mamba-MPC
[paper]: https://doi.org/10.1109/OJCSYS.2026.3724785
[preprint]: https://arxiv.org/abs/2604.13857
[video]: https://youtu.be/JZUzMLH1HeU
