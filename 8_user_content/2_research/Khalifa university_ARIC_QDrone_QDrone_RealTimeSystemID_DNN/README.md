# Real-Time System Identification (DNN + MRFT) for QDrone Control Loops

## Overview

This paper demonstrates a **real-time identify-then-tune workflow** for UAV control loops. A **Modified Relay Feedback Test (MRFT)** first forces a safe, steady oscillation; then **one steady oscillation cycle** of input/output is used by a small neural network to **select the best-matching model** from a pre-defined library (**208** candidates). The corresponding controller gains are then **looked up** and the system switches from MRFT to normal control.


---

## How the Quanser Community Can Use This (practical, right away)

- **Real-time parameter identification lab:** run MRFT on QDrone, capture one cycle, classify the model, and switch gains; measure settling time and stability margins.
- **IMU + OptiTrack sensor fusion lab for pose estimation:** reproduce the state-estimation pipeline used for the altitude/roll experiments and evaluate drift vs update rate.
- **Extend model families:** go beyond the SOIPTD assumption by adding richer model structures (e.g., coupling / cross-axis effects) and retrain on the expanded library.
- **Replace lookup PD with robust or MPC designs:** keep the same “identify → select model” step, but swap the gain-lookup controller synthesis.
- **Modernize the classifier:** replace the current NN with more modern encoders/decoders (or alternative architectures) while keeping the same one-cycle MRFT input format.

---

## Experimental Setup (as described)

- **Platform:** Quanser **QDrone**
- **Loops shown:** altitude and roll
- **State estimation:** OptiTrack + IMU (as stated in your notes)
- **Perturbation/input:** MRFT (relay-like test controller to induce oscillations)
- **Adaptation test:** payload change of **+400 g** (~30% mass increase)
- **Compute note:** example inference time is on the order of **milliseconds** (your notes mention ~5 ms CPU)

---

## Links

- **GitHub Repository:** 
https://github.com/MWahbahCC/DNN_system_ID
- **Paper (IEEE Xplore abstract):** 
https://ieeexplore.ieee.org/abstract/document/9130679
- **Paper (arXiv):** 
https://arxiv.org/abs/2004.08603
---

## Authors

Abdulla Ayyad · Mohamad Chehadeh · Mohammad I. Awad · Yahya Zweiri
