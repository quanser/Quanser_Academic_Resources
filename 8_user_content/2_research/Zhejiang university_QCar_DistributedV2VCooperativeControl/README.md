# Real-Time V2V Cooperative Control with Lease Scheduling via a Distributed Database

## Overview

This project implements and demonstrates a **real-time vehicle-to-vehicle (V2V) network cooperative control system** for **intersection (crossroad) coordination** using **Quanser QCar**.

The foundational idea is the **data-communication architecture**: each vehicle continuously writes its **own state** and **surrounding (detected objects)** into a shared **etcd “environment pool”** (a distributed key–value database). Each vehicle reads others’ entries to build a larger-than-local view of the intersection. The system uses etcd’s **Raft-based** consistency and leader failover behavior for robustness.

---

## Why This Is Foundational for QCar Users

- **Drop-in shared state for multi-QCar labs:** reuse the `state` + `surrounding` schema as a common interface for coordination, not just intersections.
- **A baseline for coordinated planning:** implement “snapshot → lease → speed enforcement” and compare against lock/FIFO-style policies with the same inputs.
- **A testbed for networked autonomy:** study how coordination changes under latency/jitter or node dropouts while keeping the same shared-state design.
- **A starting point for cooperative perception:** publish object lists into the environment pool to reduce occlusion risk by “seeing through” neighbors.

---

## Experimental Setup

- **Platform:** QCar1s.
- **Sensors / perception inputs (as described):** multi-camera setup (including RGBD) plus LiDAR; object detection/tracking with smoothing and duplicate removal.
- **Communication subsystem:** **etcd** distributed key–value database used for the shared environment pool (per-vehicle `state` and `surrounding` fields).
- **Implementation stack (as described):**
  - **Python** for sensor I/O and processing/fusion
  - **Go** for the main “sense → decide → control” loop and etcd integration

---

## Stack

**Tags:** `QCar` `V2V` `Intersection Coordination` `Lease Scheduling` `Distributed Systems` `etcd` `Raft` `Go` `Python` `Multimodal Perception`

---

## Links

- **GitHub Repository:**  
  https://github.com/Essoz/Distributed-Intersection-Traffic-Coordination-With-Lease

- **Paper (Springer chapter):**  
  https://link.springer.com/chapter/10.1007/978-981-97-5441-0_13

---

## Authors

Xinwen Zhu · Zihao Li · Yuxuan Jiang · Jiazhen Xu · Jie Wang · Xuyang Bai

**Contribution note:** X. Zhu, Z. Li, Y. Jiang, and J. Xu contributed equally to this work. This work was done during their undergraduate studies at Zhejiang University.