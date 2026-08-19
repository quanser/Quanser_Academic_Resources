# Reinforcement Learning Control for QUBE Servo 2

## Overview
This project develops and evaluates reinforcement learning control for the QUBE Servo 2 rotary inverted pendulum. A Soft Actor Critic agent is trained in a custom physics simulation to swing the pendulum upright and maintain balance, then deployed on the physical system.

The repository covers system identification, simulation, reinforcement learning, hardware deployment, and comparison with PID and LQR controllers. It also includes PPO training, domain randomization, state estimation, experimental datasets, and plotting tools.

---

## How the Quanser Community Can Use This
- A capstone reference for **reinforcement learning, nonlinear control, system identification, and simulation to hardware transfer**.
- A lab module for **controls, robotics, mechatronics, engineering, and AI courses**.
- An example of comparing learned control with **PID and LQR** on the same physical system.
- A practical workflow for identifying system parameters and improving a training simulator.
- A starting point for testing other methods such as TD3, adaptive control, model based reinforcement learning, or constrained reinforcement learning.

---

## Experimental Setup
- **Platform:** QUBE Servo 2 rotary inverted pendulum
- **Sensors:** Rotary encoders for arm and pendulum angles
- **Software and libraries:** Python, MATLAB, PyTorch, TorchRL, Gymnasium, NumPy, Numba, SciPy, Pandas, Matplotlib, PyQt, and pyqtgraph
- **Simulation:** Custom nonlinear model with Runge Kutta integration and domain randomization
- **Hardware interface:** Python serial communication with Arduino firmware
- **Training and analysis:** Parallel CPU training, hyperparameter search, live plotting, and experimental datasets

---

## Stack / Tags
`QUBE Servo 2`, `Python`, `MATLAB`, `PyTorch`, `TorchRL`, `Gymnasium`, `Soft Actor Critic`, `PPO`, `Reinforcement Learning`, `PID`, `LQR`, `Kalman Filter`, `System Identification`, `Domain Randomization`, `Simulation to Hardware`, `Inverted Pendulum`

---

## Links
- **GitHub Repository:**  
https://github.com/ModeS7/Pendulum_RL

---

## Author
Modestas Sukarevicius  
Norwegian University of Science and Technology (NTNU)