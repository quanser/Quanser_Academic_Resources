# QCar SLAM (FastSLAM)


## Overview

A Python implementation of **grid-based FastSLAM** for the **QCar1**:

- **Map:** occupancy grid (cell probability of being occupied)
- **State estimation:** particle filter (many pose hypotheses + weights)
- **Sensors used:** wheel encoders (motion update) + LiDAR (map update)

---

## What you’ll learn

- Why SLAM is a “chicken-and-egg” problem (pose vs map)
- Particle filters (predict → weight → resample)
- Occupancy-grid mapping from LiDAR
- Practical workflow: SSH to a robot, run code, retrieve outputs

---

## Links

- **GitHub Repository:**  
https://github.com/DanielMiamiU/Qcar

---

## Author

Daniel Wood (Miami University)
