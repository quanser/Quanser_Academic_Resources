# LLM Guided Cube Sorting and Stacking with QArm

## Overview

This thesis project uses the Quanser QArm to sort and stack colored cubes from natural language instructions. A user can enter a goal such as “stack blue cubes on the left and orange cubes on the right,” and a local language model selects the next action from a short list of commands that are valid for the current task state.

The **LLM decides but never drives**. YOLO perception, RGB D localization, visual servoing, inverse kinematics, motor current monitoring, and post action verification handle the physical task. The result is a constrained agentic workflow in which the language model selects high level actions, while classical robotics code executes and checks them. It is not an end to end vision language action model.

---

## How the Quanser Community Can Use This

- Reuse the legal command, strict JSON, validation, and fail loudly pattern for other LLM guided QArm tasks.
- Adapt the motor current monitoring logic for grasp confirmation, overload protection, and collision response.
- Reparameterize the wrist mounted RealSense projection chain for a different camera mount, workspace, or object layout.
- Use the experiment runner and prompt history to compare local models, prompts, command menus, and verification settings.
- Replace the cube sorting commands and verification rules to build new agentic manipulation projects such as object handover, assembly, or inventory handling.

---

## Experimental Setup

- **Platform:** Quanser QArm
- **Software:** Python, Quanser SDK and a locally hosted Ollama language model
- **Sensors:** Wrist mounted Intel RealSense RGB D camera, joint encoders, and motor current feedback
- **Decision policy:** One LLM selected command per cycle from a dynamically generated legal command list
- **Libraries / APIs:** Quanser PAL and HAL, Ultralytics YOLO, Ollama, pyrealsense2, OpenCV, and NumPy
- **Project status:** Thesis work in progress; camera offsets, current thresholds, stack geometry, and control gains are tuned for one physical setup

---

## Stack / Tags

`QArm`, `Python`, `Agentic AI`, `LLM Guided Robotics`, `Ollama`, `YOLO`, `RGB D Vision`, `Visual Servoing`, `Inverse Kinematics`, `Current Sensing`, `Cube Sorting`, `Cube Stacking`, `Robotic Manipulation`

---

## Links

* **GitHub Repository:**  
https://github.com/TomasEzFranco/LLM_Based_Manipulation

* **Video Demonstration:**  
https://www.youtube.com/watch?v=ye8d9MgdUjU

* **Author Portfolio:**  
https://tomasezfranco.github.io/

---

## Author

Tomas Franco  
M.S. Mechanical Engineering Candidate  
California Polytechnic State University, San Luis Obispo
