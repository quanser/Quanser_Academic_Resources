# Milton: An Indoor Wayfinding and Reception Robot on the Quanser QBot Platform

## Overview
Milton turns the Quanser QBot Platform into an indoor wayfinding and reception robot. A visitor types the name of a room or a person, and Milton matches it against a directory, confirms the destination ("Did you mean X? Shall I take you there?"), then drives there autonomously with lidar-based navigation, avoiding obstacles along the way. On arrival it announces itself and returns to its start point on its own. While idle, it shows an animated face, watches for nearby people with its camera, and greets them.

Everything runs onboard the robot's Jetson computer, so Milton works fully offline; a phone or laptop is only ever a remote screen for the face, camera, or map. The destination and navigation workflow is deliberately deterministic, while an optional local Ollama model makes the robot's replies more natural without ever deciding where it drives, a clean separation that keeps the safety-relevant steps predictable.

---

## How the Quanser Community Can Use This
- A ready lab or capstone project for courses in mobile robotics, ROS 2, autonomous navigation, and human-robot interaction, showing a full Nav2 stack (mapping, localization, planning, obstacle avoidance) on the QBot Platform.
- A reusable "label a point, then navigate by name" workflow: map and pin destinations once, then reach any of them just by typing its name, easily re-pointed at a new building, office, lab, or museum.
- A worked pattern for safe, predictable dialogue: confirm the destination before driving, and keep the language model out of the matching step so navigation stays deterministic.
- Add sensors and fuse them for safer, more accurate navigation, for example bringing the depth camera into obstacle avoidance alongside the lidar, or adding wheel odometry or an IMU to improve localization.
- Add speech recognition for spoken destinations, or automatic waypoint discovery so destinations don't all have to be placed by hand.

---

## Experimental Setup
- **Platform:** QBot Platform
- **On-robot compute:** NVIDIA Jetson, running everything onboard
- **Sensors:** lidar for mapping and navigation; Intel RealSense depth camera for detecting people and their distance
- **Navigation:** Nav2 with AMCL localization, a NavFn global planner, and an MPPI local controller, using lidar only
- **Mapping:** Cartographer / slam_toolbox to build the floor plan, plus a custom tool to label destinations
- **Perception and dialogue:** YOLOv8 for idle person detection, rapidfuzz for directory matching, and an optional Ollama/Llama 3.2 chatbot for small talk
- **Interaction:** type-in destinations with spoken replies (text-to-speech); no microphone or speech recognition
- **Software:** Python (application logic) and Quanser QUARC hardware driver, on ROS 2 Humble
---

## Stack / Tags
`ROS 2`, `Python`, `C++`, `Nav2`, `AMCL`, `MPPI`, `SLAM`, `YOLOv8`, `Ollama`, `Llama 3.2`, `Lidar`, `Intel RealSense`, `Service Robot`, `QBot Platform`

---

## Links
- **GitHub Repository:**  
https://github.com/miltonT2023/857_Final_Project_Code

- **Video Demonstration:**  
https://sfsu.app.box.com/s/hoonttjottngycgndjtjwetef5un9caq/file/2355536274880

- **Full Report:**  
https://sfsu.app.box.com/s/hoonttjottngycgndjtjwetef5un9caq/file/2355535947723

---

## Author
Milton Tinoco Marin, Harrison Lew, Bisum Tiwana 
San Francisco State University