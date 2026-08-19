# Healbot: Voice Controlled, LLM Powered Item Retrieval with QArm

## Overview

Healbot is a voice controlled robotic item retrieval project built with the Quanser QArm. A user can make a request such as “I’m thirsty,” and the system identifies and retrieves the most suitable available item from a shelf.

The workflow combines speech recognition, a custom YOLOv8 object detector, GPT-4o-mini for language based item selection, and classical inverse kinematics for scripted pick and place motion. Each stage has a clear role, making the project a practical example of applied AI, computer vision, human robot interaction, and robotic manipulation.

---

## How the Quanser Community Can Use This

- Use it as a student project example combining speech, computer vision, language models, and QArm control.
- Apply it in robotics, computer vision, AI, NLP, mechatronics, and human robot interaction courses.
- Extend the YOLO model and item catalog for new retrieval or assistive robotics tasks.
- Add closed loop motion, grasp confirmation, 3D localization, inventory tracking, and workspace safety.
- Use it as inspiration for an agentic robotics workflow that can rescan, ask questions, check inventory, and recover from failed actions.

---

## Experimental Setup

- **Platform:** Quanser QArm
- **Software:** Python, Quanser SDK
- **Camera:** Intel RealSense RGB D camera, using the RGB stream for YOLO detection
- **Audio input:** Microphone
- **Language model:** GPT-4o-mini for semantic item selection
- **Motion control:** Quanser inverse kinematics and fixed Cartesian waypoints
- **Libraries / APIs:** Ultralytics YOLO, OpenAI API, SpeechRecognition, OpenCV, and Quanser PAL / HAL

---

## Stack / Tags

`QArm`, `Python`, `Applied AI`, `YOLOv8`, `GPT-4o-mini`, `Computer Vision`, `Speech Recognition`, `Semantic Item Retrieval`, `Inverse Kinematics`, `Pick and Place`, `Human Robot Interaction`, `Assistive Robotics`, `Agentic Robotics`

---

## Links

* **GitHub Repository:**  
https://github.com/TomasEzFranco/Healbot

* **Video Demonstration:**  
https://www.youtube.com/watch?v=xKzFN9P7FqU

* **Author Portfolio:**  
https://tomasezfranco.github.io/

---

## Author

Tomas Franco  
M.S. Mechanical Engineering Candidate  
California Polytechnic State University, San Luis Obispo
