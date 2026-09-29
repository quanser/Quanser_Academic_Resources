# DronePropA: Propeller Fault Dataset and MATLAB Tools (Quanser QDrone 2)

## Overview

`DronePropA` shares 130 labelled QDrone 2 flights, along with MATLAB extraction and plotting scripts for propeller health monitoring. A drone can still follow its flight path with a chipped or cracked propeller without a significant loss in flight performance. **Can its sensor readings and motor commands reveal the damage?**

To explore this, the [researchers][paper] recorded **130 QDrone 2 flights** using healthy and deliberately damaged propellers across five flight paths and two speeds. The dataset has already supported work on [inner control loop diagnosis][inner], [IMU vibration classification][ensemble], and an [interpretable health scoring prototype][aas].

The QDrone 2's accessible sensing and control interfaces also make it possible to collect new data and test health monitoring methods alongside the flight controller.


---

## How the Quanser Community Can Use This

Suggested extensions to the linked studies:

- **Combine vibration and control effort:** fuse IMU features with motor commands or errors from a learned motion predictor. Compare the combined detector with each signal group alone.
- **Build a smaller live monitor:** compare the published ensemble with fewer features, one IMU, or shorter observation windows. Measure accuracy, false alarms, and processing time including feature extraction.
- **Test speed and severity robustness:** train at one speed and test at the other. Report detection of the smallest damage level within each fault type, alongside the established trajectory testing protocol.
- **Compare health scores with classifiers:** extend the AAS prototype using multiple healthy training flights to calibrate scores and warning thresholds. Compare scores and classifiers on the same held out maneuvers and speeds.
- **Add electrical evidence:** verify current channels mapped in the authors' [plotter][electrical]. Test whether current and battery voltage improve detection beyond motion and command signals under matched flight conditions.

**Split complete flights before creating training windows.** Fit feature selection, normalization, and thresholds on training data only. Keep test flights identical across compared methods.

---

## Experimental Setup

- **Platform:** Quanser QDrone 2
- **Sensing & signals:** two onboard IMUs and 14 camera OptiTrack; battery voltage, height, and individual motor and ESC commands
- **Propellers:** HQ Durable 7 x 4.5, with three damage types and three severity levels each.
- **Recording:** reported logging rate of 1 kHz; MATLAB mission generation and data processing.

---

## Dataset Contents

**130 MATLAB `.mat` files: 90 faulty and 40 healthy flights**, covering five maneuvers and two maximum speed settings.

**Maneuvers:** diagonals and perimeter of a 1 m square; stepped and direct vertical motion between 0.2 and 0.8 m; and a yaw sequence.

**Speed settings:** `SP1` = 2 m/s and 3.14 rad/s; `SP2` = 0.333 m/s and 0.52 rad/s.

---

## Stack / Tags

`QDrone 2`, `MATLAB`, `Fault Diagnosis`, `Machine Learning`, `System Identification`, `IMU`, `Health Monitoring`

---

## Links

### Original paper

- [DronePropA: Motion trajectories dataset for defective drones][paper]. Ismail et al., *Data in Brief*, 2025. Experiment design, signal mappings, and filename labels.

### Dataset and MATLAB tools

- [DronePropA, Mendeley Data, version 1][dataset]. Flight recordings, CC BY 4.0.
- [Authors' MATLAB extraction and plotting scripts][code].

### Papers using DronePropA

- [Fault Diagnosis of Drone Propellers using Inner Loop Dynamics][inner]. Elshaar et al., ICCAD 2025. The original team's diagnosis method based on inner control loop signals.
- [Intelligent fault detection of UAV propellers through time-domain vibration analysis and ensemble learning][ensemble]. Mohammed et al., *Aerospace Systems*, 2026. Independent IMU feature and ensemble study; reports **97.9% accuracy** with leave one trajectory out validation.
- [A Metamorphic Artificial Age Score (AAS) Decision-Support Prototype for Flight-Log-Based Drone Propeller Health Monitoring][aas]. Seyma Yaman Kayadibi, 2026 **preprint**. Independent health scoring study using four selected flights; not a full dataset classifier benchmark.

---

## Authors

Mohamed A.A. Ismail; Mohssen E. Elshaar; Ayman Abdallah; Quan Quan.

**Affiliations:** Interdisciplinary Research Center for Aviation and Space Exploration, King Fahd University of Petroleum and Minerals (KFUPM); Beihang University.

[dataset]: https://doi.org/10.17632/ftdyxrr3c5.1
[paper]: https://doi.org/10.1016/j.dib.2025.111589
[code]: https://github.com/DrIsmailCode/DronePropA-Motion-Trajectories-Dataset
[electrical]: https://github.com/DrIsmailCode/DronePropA-Motion-Trajectories-Dataset/blob/main/plot_daq_qdrone2.m.txt
[inner]: https://doi.org/10.1109/ICCAD64771.2025.11099495
[ensemble]: https://doi.org/10.1007/s42401-026-00460-7
[aas]: https://arxiv.org/abs/2608.18088
