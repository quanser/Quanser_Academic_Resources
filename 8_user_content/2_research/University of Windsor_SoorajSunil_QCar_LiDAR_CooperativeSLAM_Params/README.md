# Feature-Based Occupancy Grid Map Merging for Collaborative SLAM (QCar)

![Occupancy Grid Map Fusion Overview](https://raw.githubusercontent.com/soorajsunil/Occupancy-Grid-Map-Fusion/main/Resources/overview.png)
<!-- Image source: soorajsunil/Occupancy-Grid-Map-Fusion repository (branch: main). -->

## Overview

Collaborative SLAM is powerful, but it quickly becomes messy when different robots (or the same robot with different settings) produce **heterogeneous occupancy grids** (different resolutions, scan/update rates, and drift). Naïve overlays often fail because maps may be **rotated, shifted, scaled, or slightly distorted**.

This work treats occupancy grids as **images** and performs **feature-based registration** to estimate a reliable transform between maps. It then **Bayes-fuses** aligned grids into a single **order-independent** global map. A companion repo provides **real QCar 2D LiDAR scans** and a MATLAB Graph-SLAM demo to generate example occupancy maps.

---

## How the Quanser Community Can Use This

- Run a **heterogeneous map-merging lab**: build two occupancy grids of the same space with different **r (cells/m)** and **T (Hz)** (or from two robots).
- Implement the **core pipeline**: free-space image → **KAZE + SIFT + MSAC** alignment → **Bayesian fusion** (order-independent).
- Do a **detector shootout**: compare **ORB / KAZE / SURF / SIFT** using inliers/precision, runtime, and rotation error.
- Validate with **navigation**: plan on the fused map using **RRT** (or A*) and observe how fusion quality impacts paths.
- Package it as a reusable **module**: ROS node or MATLAB block (`/map` → `/global_map`) and extend to multi-map (hierarchical) fusion or camera+LiDAR augmentation.

---

## Experimental Setup

- **Platform:** Quanser QCar (data collection)
- **Sensor:** 2D LiDAR (scan data)
- **Local mapping demo:** MATLAB Navigation Toolbox Graph-SLAM → occupancy grid maps
- **Map alignment:** keypoint detection + descriptor matching + robust transform estimation (MSAC/RANSAC-style)
- **Fusion:** Bayesian grid fusion (order-independent)

---

## Stack / Tags

**Tags:** `QCar` `2D LiDAR` `Collaborative SLAM` `Occupancy Grid` `Image Registration` `MATLAB` `Navigation Toolbox` `Computer Vision Toolbox`

---

## Links

- **GitHub Repository:**  
  https://github.com/soorajsunil/Occupancy-Grid-Map-Fusion

- **Data + SLAM Demo Repo (QCar LiDAR scans):**  
  https://github.com/soorajsunil/Lidar-Data-Multi-Robot-SLAM

- **Paper: Feature-Based Occupancy Map-Merging for Collaborative SLAM:**  
  https://www.mdpi.com/1424-8220/23/6/3114

- **Paper: LiDAR-Based Cooperative SLAM with Different Parameters:**  
  https://ieeexplore.ieee.org/document/10097789

---

## Authors

Sooraj Sunil · Saeed Mozaffari · Rajmeet Singh · Behnam Shahrrava · Shahpour Alirezaee
