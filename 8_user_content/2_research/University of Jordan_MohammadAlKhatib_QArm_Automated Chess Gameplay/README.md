# Automated Chess Gameplay With Computer Vision and A Robotic Arm

## Overview
This repo and paper present a **modular perception-to-action chess automation workflow built around the Quanser QArm**. The system begins with a fixed top-view camera, uses a fine-tuned **YOLOv8x** model to detect the chessboard and pieces, converts those detections into **FEN** board state, queries **Stockfish** for the next move, and then executes that move through **MATLAB/Simulink** as a calibrated QArm pick-and-place action. Strategically, this is more than a chess demo: it is a compact example of how to connect **vision, symbolic state estimation, decision-making, and physical manipulation** in a structured tabletop task. The paper reports the full real-world system, while the public project materials support reproducibility of the core perception, state-construction, engine-integration, and robot-motion pipeline.

## How Quanser Users Can Use This
- Use it as a **teaching example for full-stack robotic autonomy on QArm**, showing how perception feeds decision-making and then becomes physical actuation.
- Reuse the **board-to-state pipeline** as a template for other structured workspaces where a camera first detects a workspace and then maps objects into symbolic locations or slots.
- Reuse the **square-to-coordinate calibration idea** for grid-based QArm tasks such as part placement, tray handling, or workspace indexing.
- Use it as a **baseline for vision-guided pick-and-place** before moving to harder manipulation problems with more clutter, uncertainty, or variable objects.
- Extend it toward **workspace-aware autonomy**, where the QArm first identifies free space, piece geometry, and workspace constraints, then plans its own grasp sequence or motion path instead of relying only on fixed calibrated moves.
- Build a stronger next version using **depth or stereo sensing**, more adaptive grasping, and more robust visual feedback, which aligns well with the paper’s own future-looking recommendations.

## Experimental Setup
**Platform:** Quanser QArm  
**Sensors:** Fixed top-view smartphone RGB camera  
**Compute / Control:** Laptop for YOLOv8x + Stockfish, desktop running MATLAB/Simulink  
**Dataset:** 173 top-view chessboard images, 13 classes, 4163 annotated object instances, with augmentation expanding training data to 363 images  
**Engine / State Representation:** Stockfish 16.1 + FEN  
**Environment:** Real tabletop chess setup, with **QLabs Virtual QArm** also used to refine the Simulink motion workflow before physical trials

## Stack
**Tags:** QArm, YOLOv8x, Stockfish, FEN, Python, MATLAB, Simulink, computer vision, robotic manipulation, pick-and-place, tabletop autonomy

## Links
**GitHub Repository:**  
https://github.com/Mohammadjalkhatib/Automated-Chess-Gameplay-with-Computer-Vision-and-a-Robotic-Arm

**Paper:**  
https://doi.org/10.1002/eng2.70607

**Dataset:**  
https://universe.roboflow.com/mohammadjalkhatib/chess_dataset_topview

**Model:**  
https://huggingface.co/Mohammadjalkhatib/chess_yolo

## Authors
Mohammad AlKhatib · Fahed Jubair · Mohammad Al Mashagbeh · Moath Khaleel · Samah Rahamneh