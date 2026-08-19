# QCar Lane Following: Camera-Based Vision and Control for Sim and Real QCar

## Overview
This is a ROS 2 workspace for a camera-based lane-following QCar, developed for a university robotics course and the TMR 2026 competition. A computer-vision node detects lane lines from the camera and outputs a target point; a Pure Pursuit controller turns that into steering and speed commands. The same code runs in Gazebo simulation and on the physical QCar2 by changing one parameter. Quanser's official examples navigate from a pre-built map; this project does lane detection instead, which Quanser's stack does not include.

---

## How the Quanser Community Can Use This
- A camera-based lane-following example for the QCar: a complete perception-to-steering loop that detects lane lines and drives toward them.
- A ready teaching kit spanning several courses: Introduction to ROS 2, Autonomous Mobile Robots, Computer Vision for Robotics, Control Systems / Vehicle Dynamics, and robotics capstone or senior design.
- A layered, swappable architecture: perception and control are separate nodes over topics, so an instructor can hand students just the vision layer or just the control layer and have them plug in their own while the rest keeps working.
- A worked sim-to-real pattern: a resolution-independent region of interest and dual-platform message switching let the same nodes run in Gazebo and on hardware without retuning.
- A no-hardware-required option: the bundled generic Ackermann and differential-drive robots run the same course structure for classes without a QCar.
- A base for extending with sign detection, obstacle avoidance, localization, path planning, or parking.

---

## Experimental Setup
- **Platform:** Quanser QCar2, run on both real hardware and Gazebo simulation
- **Software:** ROS 2 (Humble/Jazzy)
- **Simulation:** Gazebo (Fortress/Harmonic), with `ros_gz_bridge` and `robot_localization` (EKF)
- **Control:** Pure Pursuit for steering and speed (speed-scaled lookahead); a C++ Ackermann controller converting drive commands into per-wheel steering and speed, wired into `ros2_control`
- **APIs / Libraries:** OpenCV for the lane detection pipeline (HLS color segmentation, bird's-eye-view homography, adaptive lane-width estimate); `ros2_control`
- **Development languages:** Python and C++


---

## Stack / Tags
`ROS 2`, `Gazebo`, `OpenCV`, `Python`, `C++`, `Lane Detection`, `Pure Pursuit`, `Ackermann Steering`, `Sim-to-Real`, `QCar`, `Quanser SDK`

---

## Links
- **GitHub Repository:**  
https://github.com/dsosa114/movilidad_inteligente

---

## Author
Daniel Sosa  
Tecnológico de Monterrey, Monterrey, Nuevo León, Mexico