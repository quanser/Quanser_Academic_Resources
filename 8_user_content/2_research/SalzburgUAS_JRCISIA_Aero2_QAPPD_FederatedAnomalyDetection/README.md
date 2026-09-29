# Federated Anomaly Detection for Repetitive Processes (Quanser Aero 2)

## Overview

This project investigates a modern **industrial AI challenge:** how machine learning can learn the normal behavior of a repetitive process and detect changes in its timing, position, or electrical signals, even when the training data is distributed across multiple clients instead of stored in one place.

The researchers use a Aero 2 to generate repetitive motion data inspired by pick and place operations, then compare **DeepAnT, LSTM-AE, USAD, TranAD, and MTAD-GAT** under **centralized, federated, and hierarchical federated learning**. The models analyze recorded motion and electrical signals and produce anomaly scores rather than motor commands.

The project also releases **QAPPD**, ten independent training and test pairs, giving others a reusable starting point for anomaly detection and distributed learning experiments.

---

## How the Quanser Community Can Use This

- **Compare learning strategies:** train the same detector centrally, with federated learning, and with hierarchical federated learning to study how distributed training changes performance.
- **Build new anomaly detectors:** reuse QAPPD with statistical methods, autoencoders, forecasting models, or newer time series architectures.
- **Ask whether AI adds value:** compare neural anomaly scores with simple timing, position, voltage, or tracking error alarms on the same recordings.
- **Study sensor combinations:** test whether voltage, current, motor speed, and motion signals together improve detection compared with individual signal groups.
- **Create new Aero 2 clients:** collect additional repetitive trajectories or anomaly types in another lab and study cross client generalization, personalization, or non identical operating conditions.

---

## Experimental Setup

- **Platform:** Quanser Aero2 :2 DOF Helicopter
- **Anomalies:** defined changes in timing, position, and motor voltage.
- **Models:** DeepAnT, LSTM-AE, USAD, TranAD, and MTAD-GAT.
- **Software and language:** Python and Quanser SDK, with PyTorch Lightning, and Flower.

---

## Dataset Contents

**QAPPD contains ten independent training and test pairs.** Training recordings represent normal operation, while test recordings contain normal and abnormal behavior.

The dataset can be used independently of the federated learning code, so researchers can develop and evaluate their own anomaly detection methods without recreating the Aero 2 experiments first.

---

## Stack / Tags

`Aero 2`, `Python`, `Anomaly Detection`, `Multivariate Time Series`, `Federated Learning`, `Industrial AI`, `Machine Learning`

---

## Links

- **Paper:** [Federated Learning for Multivariate Time Series Anomaly Detection in Industrial Automation][paper]
- **Code:** [industrial-federated-learning][code]
- **Dataset:** [Quanser Aero 2 Pick-and-Place Dataset (QAPPD)][dataset]

---

## Authors

Khayyam Nosrati; Martin Uray; Saverio Messineo; Olaf Sassnick; Stefan Huber.

Josef Ressel Centre for Intelligent and Secure Industrial Automation, Salzburg University of Applied Sciences, Austria. Martin Uray is also affiliated with Paris Lodron University of Salzburg.

[paper]: https://arxiv.org/abs/2605.27486
[code]: https://github.com/JRC-ISIA/industrial-federated-learning/
[dataset]: https://doi.org/10.5281/zenodo.20287835
