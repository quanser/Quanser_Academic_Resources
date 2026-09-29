# AirScanner: Laser Vibration Dataset for Propeller Fault Diagnosis (Quanser QDrone 2)

## Overview

Another propeller health dataset led by researchers at the **Interdisciplinary Research Center for Aviation and Space Exploration at KFUPM**, this time looking at the problem from **outside the drone**.

Instead of using onboard signals, the researchers point a Laser Doppler Vibrometer at a hovering QDrone 2 and measure its vibration without touching the aircraft. **Can propeller damage be detected from an external vibration measurement?**

The dataset contains measurements for a healthy propeller and nine combinations of fault type and severity. Each measurement lasts about one second while the QDrone 2 maintains a stable hover.

This complements the earlier [**DronePropA**](../KFUPM_MohamedIsmail_QDrone2_DronePropA_PropellerFaultDataset/) resource. DronePropA explores propeller health using **onboard IMU, flight, and motor command signals**, while this dataset studies the same problem using an **external laser vibration sensor**. The offboard approach is especially interesting for commercial drones where access to onboard sensing or flight controller software may be limited.

---

## How the Quanser Community Can Use This

- **Build your own detector:** extract RMS, kurtosis, and crest factor, then compare a small neural network with a decision tree or SVM. Measure accuracy, false alarms, and processing time.
- **Detect smaller damage:** compare statistical features with frequency or wavelet features. Report which features improve detection at the lowest severity level within each fault type.
- **Reduce measurement time:** compare shorter segments with complete recordings. Test how much data is needed before smaller faults become harder to detect.
- **Reuse DronePropA methods:** adapt a vibration feature or classifier workflow from DronePropA to these laser recordings. Evaluate each dataset separately; the downloads are not documented as synchronized sensor pairs.
- **Build a combined monitoring experiment:** collect synchronized onboard and LDV recordings on QDrone 2, then compare each source alone with both together (Signal Processing, Machine Learning, or Robotics projects).

**Split original measurements before creating training windows.** Keep all windows from one measurement in the same split, and fit preprocessing on training data only.

---

## Experimental Setup

- **Platform:** Quanser QDrone 2
- **Sensors:** external Polytec VibroGo LDV measuring surface vibration velocity, and OptiTrack
- **Propellers:** HQ Durable 7 x 4.5, with edge cuts, cracks, and surface unbalance at three severity levels each.

---

## Dataset Contents

The paper describes **50 measurements across 10 classes:** healthy propellers plus nine combinations of fault type and severity, with **five measurements per class**.

**Recording:** Section 4.1 reports one second per measurement at **4,410 Hz**, with vibration velocity in m/s.

---

## Stack / Tags

`QDrone 2`, `Laser Doppler Vibrometry`, `Vibration Analysis`, `Fault Diagnosis`, `Machine Learning`, `DeepELM`, `Health Monitoring`

---

## Links

### Original paper

- [Offboard Fault Diagnosis for Large UAV Fleets Using Laser Doppler Vibrometer and Deep Extreme Learning][paper]. Ismail et al., *Automation*, volume 7, article 6. AirScanner method and experimental setup.

### Dataset

- [Offboard laser Doppler vibrometry dataset for UAV propeller fault diagnosis][dataset]. Zenodo, version 2. Labelled measurements and file documentation.

### Related resource: DronePropA

- [DronePropA: Propeller Fault Dataset and MATLAB Tools][dronepropa-community]. Related Quanser Community entry for onboard monitoring.
- [DronePropA dataset][dronepropa] and [original data paper][dronepropa-paper]. Onboard recordings from 130 QDrone 2 flights across five maneuvers and two speed settings.

---

## Authors

**Paper:** Mohamed A.A. Ismail; Saadi Turied Kurdi; Mohammad S. Albaraj; Christian Rembe.

**Dataset release:** Luttfi Al-Haddad (data manager).

**Affiliations:** Interdisciplinary Research Center for Aviation and Space Exploration and Aerospace Engineering Department, King Fahd University of Petroleum & Minerals (KFUPM); Al-Bayan University; Clausthal University of Technology.

[paper]: https://doi.org/10.3390/automation7010006
[dataset]: https://zenodo.org/records/21203159
[dronepropa]: https://doi.org/10.17632/ftdyxrr3c5.1
[dronepropa-paper]: https://doi.org/10.1016/j.dib.2025.111589
[dronepropa-community]: ../KFUPM_MohamedIsmail_QDrone2_DronePropA_PropellerFaultDataset/
