# Reinforcement Learning and Learned-Model MPC Benchmarks on Qube, Ball Balancer, and Cartpole (Simulation)

## Overview
This repo implements and evaluates two learning-based control approaches across three **simulated Quanser-style systems**: a **Qube Servo (simulated rotary pendulum)**, a **Ball Balancer (simulated)**, and a **Cartpole Swing-up (simulated)**.

- **TRPO** is used as a **model-free** RL baseline.
- **MPC here is model-based RL**: it learns an approximate **dynamics model from data**, then uses that learned model for **finite-horizon planning** (not just classic MPC).

---

## How the Quanser Community Can Use This 
- Teach **model-free vs model-based RL** using Quanser-style simulated plants.
- Use as an end-to-end lab: train TRPO, learn the dynamics model, run MPC planning, then compare behaviors.
- Benchmark MPC optimizers (**ABC vs Random Sampling vs Cannon**) as a planning tradeoff exercise.
- Use as a capstone base: redesign rewards (especially for cartpole swing-up) and re-evaluate policy behavior.
- **Optional extension:** port the trained policies / control logic to real Quanser hardware (where available) to compare sim vs real behavior.

---

## Experimental Setup
- **Mode:** Simulation (rendered rollouts / recorded videos)
- **Plants (simulated):** Qube Servo rotary pendulum; Ball Balancer; Cartpole swing-up

---

## Stack / Tags
`Python`, `Reinforcement Learning`, `TRPO`, `Model-based RL`, `Learned dynamics`, `MPC planning`, `ABC optimizer`

---

## Links
- **GitHub Repository:**  
https://github.com/gongchenooo/CS339-Quanser-Robots
- **Report (PDF):** 
https://github.com/gongchenooo/CS339-Quanser-Robots/blob/master/Report%20for%20Project%20Two.pdf
