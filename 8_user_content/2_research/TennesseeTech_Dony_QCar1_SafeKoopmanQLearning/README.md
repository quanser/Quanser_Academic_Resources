# SafeQ: Learning Controllers with Safety Constraints (Quanser QCar 1)

## Overview

`SafeQ` explores **learning feedback controllers from data while accounting for motion limits**. It combines Q learning with Koopman coordinates, which provide a simpler representation of nonlinear behavior for control. The learning uses least squares rather than a large neural network.

The project shares **MATLAB control examples and a Python QCar experiment in the QLabs Cityscape digital twin**. The vehicle example learns steering from recorded motion and uses a control barrier function filter to check proposed commands against predicted tracking limits. Researchers can reuse these components to compare learned control, conventional feedback, and safety filtering.

---

## How the Quanser Community Can Use This

- **Compare steering methods:** test learned steering against Stanley and identified model LQR on the same route. Compare tracking error, boundary crossings, and steering effort.
- **Study the safety mechanisms:** compare barrier penalties and filtering separately in QLabs. Record filter interventions and whether the learned or fallback gain is deployed.
- **Test learning conditions:** vary exploration duration, vehicle speed, and measurement noise. Examine how the learned gains, tracking, and computation time change.
- **Explore nonlinear control:** change the candidate features and initial conditions in the MATLAB Koopman example. Compare prediction accuracy and the calculated safety region.
- **Test on hardware, then extend to other Quanser plants:** : transfer the QLabs experiment to a physical QCar after verifying the hardware interface and stopping limits. Compare digital twin and hardware performance, then adapt the learning workflow to a Qube pendulum or Aero 2 with new state definitions, training data, and constraints.
---

## Experimental Setup

- **Platform:** QLabs Virtual QCar Cityscape; separate MATLAB numerical examples.
- **Language and libraries:** MATLAB; Python with NumPy, OpenCV, PyQtGraph, and Quanser SDK.

---

## Stack / Tags

`QCar 1`, `QLabs`, `MATLAB`, `Python`, `Q Learning`, `Koopman`, `Control Barrier Functions`

---

## Authors

Md Nur-A-Adam Dony; Syed Ali Asad Rizvi.

Tennessee Technological University.

---

## Links

- **Repository:** [Safe-Koopman-Qlearning](https://github.com/AdamDony/Safe-Koopman-Qlearning). Source code and setup instructions.
- **Demo:** [QCar 1 in the QLabs digital twin](https://github.com/AdamDony/Safe-Koopman-Qlearning#demo-video).
- **Manuscript citation:** [Model-Free, Optimal, and Safe Q-Learning in Koopman Eigenfunction Coordinates](https://github.com/AdamDony/Safe-Koopman-Qlearning#citation). Listed in the repository as under review at IEEE Transactions on Control Systems Technology, 2026; this link is the citation, not the manuscript.