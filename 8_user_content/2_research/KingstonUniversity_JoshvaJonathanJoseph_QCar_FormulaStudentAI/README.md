# Formula Student AI Inspired QCar Autonomous Navigation in QLabs

## Overview
This project is an AI-based autonomous racing stack developed for the virtual QCar, driving it around a Formula Student AI style track marked by blue cones on the left and yellow cones on the right. It generates a cone track, then captures and labels images to train a YOLO cone detector, and uses that detector to navigate the track, estimate the car's position, record a lap, and replay that lap as a fallback when needed. Everything runs in the QLabs digital twin, adding a cone-track racing workflow alongside Quanser's lane-following labs.

---

## How the Quanser Community Can Use This
- A capstone example that joins several SDCL skill areas (state estimation, object detection, vehicle control, path logging) into one working closed-loop system.
- A followable example dataset workflow (capture, annotate, merge classes, train YOLOv8) that instructors can repurpose for any object class, not just cones.
- A record-and-replay path approach that is simple to build end to end, useful for contrasting with roadmap-based planning in a course discussion.
- A side-by-side comparison of three autonomy strategies: reactive vision, 3-state EKF localisation, and an extended 6-state EKF.
- A spline-based cone-track generator for QLabs, adding a Formula Student style layout to the environment.
- A complete, self-contained workflow that students can extend, organise, and refactor into a more rigorous project.

---

## Experimental Setup
- **Platform:** QLabs(QCar digital twin)
- **Perception:** camera-based cone detection with a custom two-class YOLOv8 model
- **Localisation:** 3-state and 6-state Extended Kalman Filters
- **Sensor inputs:** simulation-derived position and IMU (for the EKF experiments), plus cone-based visual odometry
- **Control:** cone-centre tracking with confidence-weighted fusion of vision, recorded path, and EKF state
- **Languages and libraries:** Python, Quanser QLabs (`qvl`) and PAL (`pal`), OpenCV, PyTorch, YOLO, NumPy, SciPy
---

## Stack / Tags
`Python`, `QCar`, `QLabs`, `Formula Student AI`, `YOLOv8`, `OpenCV`, `PyTorch`, `Extended Kalman Filter`, `Sensor Fusion`, `Cone Detection`, `Path Tracking`, `Digital Twin`

---

## Links
- **GitHub Repository:**  
https://github.com/buntydjoseph-dot/Formula-Student-AI-QCar-Autonomous-Navigation

---

## Author
Joshva Jonathan Joseph  
Kingston University