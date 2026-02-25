# RL Generalization for Nonlinear Systems via Dual-Scale Homogeneity Transformations

## Overview

Reinforcement Learning (RL) policies trained for one “nominal” system often **fail when physical parameters change** (mass, length, cable length, etc.). This paper proposes a lightweight alternative to heavy sim-to-real tricks: keep **one nominal RL policy** and wrap it with **physics-derived scaling transforms** so the policy input/output are normalized across parameter variations.

The authors call this idea **dual-scale homogeneity transformations**: a parameter-dependent scaling law that “homogenizes” the dynamics so the same RL policy remains effective across different system parameters.

---

## How the Quanser Community Can Use This

- **Fast start for teaching:** use the provided MATLAB code to show a simple recipe: *one RL policy + a scaling wrapper = robustness across parameter changes*.
- **Low-compute robustness alternative:** when you can write down a reasonable model, replace expensive domain randomization with physics-based transforms (much cheaper to iterate).
- **Hardware-ready RL pattern:** apply the same wrapper idea to Quanser rigs where a dominant parameter changes (length, mass, inertia), and test generalization without retraining.
- **QDrone research hook:** treat **cable length changes** as a controlled “parameter shift,” then extend with payload mass changes, wind/disturbances, or different swing targets.
- **Unknown parameters:** replicate the paper’s “estimate parameters online” direction (RLS-style) to handle real-time variations and sensor noise.

---

## Experimental Setup

**System 1: Inverted pendulum (proof-of-concept)**  
- Derives an analytic scaling law so a nominal RL policy can generalize across pendulum mass/length changes.  
- Includes an extension where parameters are **estimated online** (RLS) to update the scaling in real time.

**System 2: QDrone with slung load (hardware demonstration)**  
- **Platform:** Quanser QDrone carrying a suspended payload  
- **Ground truth:** OptiTrack at **250 Hz**; load angle inferred from relative positions  
- **Payload:** **62 g** with 3 markers  
- **Nominal cable length:** **0.5 m**; varied case **0.75 m**  
- Notes practicalities such as additional dynamics modeled approximately as a time delay with delay compensation.

---

## Stack / Tags

**Tags:** `QDrone` `Reinforcement Learning` `DDPG` `Sim-to-real` `Homogeneity transforms` `Parameter variation` `RLS` `OptiTrack` `MATLAB`

---

## Links

- **Code Source (MATLAB Central File Exchange):**  
  https://www.mathworks.com/matlabcentral/fileexchange/154782-reinforcement-learning-with-homogeneity-transformations

- **Paper (arXiv):**  
  https://arxiv.org/abs/2311.05013

- **Video (paper-linked):**  
  https://www.youtube.com/watch?v=fdC0gHXzwdE

---

## Lab / Affiliation

Khalifa University (Abu Dhabi, UAE), Advanced Research and Innovation Center (ARIC)

---

## Authors

Abdel Gafoor Haddad · Igor Boiko · Yahya Zweiri
