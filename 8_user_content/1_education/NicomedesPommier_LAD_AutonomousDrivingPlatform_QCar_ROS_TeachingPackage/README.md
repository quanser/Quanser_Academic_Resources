# L.A.D (Learn Autonomous Driving): A Browser-Based Teaching Platform for ROS 2 and Autonomous Driving

## Overview
L.A.D is a browser-based platform for teaching a ROS 2 and autonomous-driving course. Students open a web page, work through a 12-unit curriculum, and drive a browser-based QCar simulation to complete graded objectives, with no per-student install.

Each lesson page includes a code editor, a Linux terminal running in a shared ROS 2 container, and a 3D view of the QCar. 

The simulation runs in two modes behind one interface: a lightweight client-side mode (Three.js + Rapier) used by most lessons, and a Gazebo world with a physics engine and simulated LIDAR for the sensing track. 

The 12 units run in order: Introduction, Vehicle Dynamics, ROS 2 Concepts, Sensing, ROS 2 Advanced, Transformations, Perception, Simulation, Planning, Control, AI, and Safety V&V.

---

## How the Quanser Community Can Use This
- A way to run a ROS 2 course with no per-student install: students need only a browser pointed at one self-hosted machine.
- A structured 12-unit curriculum that instructors can use, adapt, or replace with their own units, levels, and objectives through the admin panel.
- Behavior-based grading: objectives can be marked complete automatically when a ROS 2 topic reaches its target value.
- An integrated browser coding environment: a Monaco editor and a Linux terminal (via `docker exec` into a shared ROS 2 container) inside the lesson page.
- Admin-enabled connection to a physical QCar2 over SSH, for a live camera and telemetry view alongside the lessons (viewing only, not full robot control from the browser).
- Local and Docker Compose deployment workflows, plus an experimental Kubernetes path.

---

## Experimental Setup
- **Platform:** QCar2
- **Software:** ROS 2, Django backend, React frontend
- **Simulation:** browser physics (Three.js + Rapier) by default; Gazebo with simulated LIDAR for the lidar lesson
- **Control:** ROS 2 topics over rosbridge
- **APIs / Libraries:** ROS 2 Humble, rosbridge, ROSLIB.js, Three.js / Rapier, Monaco, xterm.js
- **Development languages:** Python and JavaScript
---

## Stack / Tags
`ROS 2`, `Django`, `React`, `Docker`, `Three.js`, `Rapier`, `rosbridge`, `WebSocket`, `Robotics Education`, `Web IDE`, `QCar2`

---

## Links
- **GitHub Repository:**  
https://github.com/NicomedesPommier/L.A.D

---

## Authors
**Lead Developer:** Nicomedes Pommier  
**Contributors:** Sapetor, Andrés Peters, Mario Flores