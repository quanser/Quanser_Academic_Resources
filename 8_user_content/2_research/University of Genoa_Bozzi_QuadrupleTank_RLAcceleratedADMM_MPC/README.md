# RL Accelerated ADMM for Nonlinear MPC (Quanser Quadruple Tank)

## Overview

`RL Accelerated ADMM` explores how reinforcement learning can reduce the computation needed to control water levels in four interconnected tanks using nonlinear Model Predictive Control (MPC).

A Soft Actor Critic (SAC) agent selects starting guesses and adjusts the penalty parameter of the Alternating Direction Method of Multipliers (ADMM) solver. **The optimizer calculates the pump commands; the neural network tunes the solver rather than replacing the controller.**

The paper reports fewer solver iterations with comparable water level tracking in numerical simulations and experiments on physical Quanser hardware.

---

## How the Quanser Community Can Use This

- **Start with the simulation:** explore the provided tank model, training workflow, and controller comparisons.
- **Compare solver strategies:** evaluate fixed penalty settings, residual balancing, and RL assistance using computation time, solver iterations, and tracking error.
- **Extend the research:** investigate starting guesses, penalty updates, prediction horizons, and disturbances.
- **Connect control and learning:** use the tank example to study how RL can assist an optimization algorithm without replacing it (Advanced Controls / Reinforcement Learning).

---

## Experimental Setup

- **Platform:** Two Quanser Coupled Tanks systems configured as a quadruple tank plant.
- **Core method:** Nonlinear MPC, consensus ADMM, and SAC reinforcement learning.
- **Language and simulation:** Python RK4 model.
- **Sensors:** Four water levels measured by pressure sensors; two pump voltage commands.
- **Paper setup:** 0.5 s sampling; pump inputs from 0 to 12 V. The policy is trained in simulation and used on hardware without further training.

---

## Stack / Tags

`Python`, `Nonlinear MPC`, `ADMM`, `Reinforcement Learning`, `SAC`, `Optimization`, `Coupled Tanks`

---

## Links

- **Repo:** [Accelerated ADMM with RL Meta Optimization](https://github.com/Bozzi96/Accelerated-ADMM-with-RL-meta-Optimization)
- **Paper:** [Accelerated Alternating Direction Method of Multipliers via Reinforcement Learning Meta-Optimization for Nonlinear Model Predictive Control](https://doi.org/10.1109/TASE.2026.3705265)
- **Dataset:** `data/admm_training_dataset.npz` (in repo)
- **Trained policy:** `model/best_model.zip` (in repo)
---

## Authors

Alessandro Bozzi; Enrico Zero; Roberto Sacile

DIBRIS, University of Genoa, Italy.

For questions about the code or issues you encounter, open a GitHub issue, or contact Alessandro Bozzi at [alessandro.bozzi@edu.unige.it](mailto:alessandro.bozzi@edu.unige.it).