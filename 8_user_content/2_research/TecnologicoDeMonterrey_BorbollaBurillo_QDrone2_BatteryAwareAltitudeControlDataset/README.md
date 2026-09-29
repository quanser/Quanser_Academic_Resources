# Battery Aware Altitude Control Dataset (Quanser QDrone 2)

## Overview
This dataset shares **QDrone 2 flight recordings and a documented experimental procedure** for developing voltage sag predictors and battery aware altitude controllers and climb strategies.

**QDrone 2’s open architecture design** makes this work extendable: researchers can modify controllers and climb commands, then record flight signals alongside battery voltage, motor current, and electronics current.

The [paper][paper] compares cascaded Model Predictive Control (MPC) with MPC plus a **Dynamic Battery Aware Auxiliary Reference (DBAR)** system. DBAR adjusts the altitude target before it reaches the controller, reducing aggressive thrust demand as battery voltage margin decreases.

---

## How the Quanser Community Can Use This

- **Add battery awareness to Quanser's existing PID.** Use the [QDrone 2 PID example][pid]. First adapt Table 1's procedure to characterize sag with your PID settings and battery, within safe limits. Then fit your own relationship and add an altitude reference limiter. Reuse the procedure and use MPC coefficients in the paper.
- **Fit a voltage sag predictor.** Use Figures 7 and 8 to map altitude reference gap, `delta`, to peak voltage sag. Compare interpolation, a refitted quadratic, and simple regression. Produce a fitting script and callable predictor. This is a small regression task, not training a general flight controller.
- **Learn a short horizon climb response model.** Use altitude, battery voltage, and motor voltage histories from Figures 9, 11, and 13 to predict future altitude and battery voltage. Fit a small time series model; hold out whole maneuvers or flights for testing. Add PID recordings and varied climbs before using predictions to select new commands.
- **Build and compare climb planners.** On the same PID, compare abrupt commands, fixed ramps, minimum jerk profiles, and a battery adaptive reference. Match climb distance and duration where feasible to separate battery awareness from simply slowing down. Report tracking RMSE, minimum voltage, and energy per completed climb (Controls, Robotics, System Identification).

---

## Dataset Contents

[Zenodo v2][data]: **19 Excel files plus a README, 36.6 MB**. Paired files use **`a` for MPC** and **`b` for MPC with DBAR**.
- **Paper:** [Dynamic battery-aware auxiliary reference system for improving real-time model predictive control implementation in quadrotors](https://www.tandfonline.com/doi/full/10.1080/21642583.2026.2671488#d1e342)

---

## Experimental Setup

- **Platform:** Quanser QDrone 2
- **Sensors:**  OptiTrack Flex13 motion tracking, onboard IMU, and battery voltage feedback
- **Original controller:** cascaded linear MPC, with and without DBAR

---

## Stack / Tags

`QDrone 2`, `MPC`, `PID`, `System Identification`, `Battery Management`, `Flight Data`

---

## Links

- **Dataset and README:** [Experimental Setup and Experimental Results, Zenodo v2][data]
- **Paper:** [Dynamic battery-aware auxiliary reference system for improving real-time model predictive control implementation in quadrotors][paper]
- **Quanser code:** [QDrone 2 position control][pid], including `QD2_DroneStack_PID_2021a.slx`; separate from the authors' MPC.

---

## Authors

Patricio Borbolla-Burillo; David Sotelo; Antonio Favela-Contreras; Francisco Beltran-Carbajal; Hugo Yañez-Badillo; Carlos Sotelo.

Tecnológico de Monterrey; Universidad Autónoma Metropolitana; Tecnológico de Estudios Superiores de Tianguistenco (TecNM).

[data]: https://zenodo.org/records/19464105
[paper]: https://www.tandfonline.com/doi/full/10.1080/21642583.2026.2671488
[pid]: https://github.com/quanser/Quanser_Academic_Resources/tree/dev-windows/5_research/autonomous_vehicles/qdrone2/position_control
