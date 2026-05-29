# Lane Centering and Following

## Overview
Yes. Here is the cleaned version in your wording:

This repo is a **lightweight, real-time lane-following stack for QCar**, built in MATLAB/Simulink. It combines simple, low-cost components that run reliably on the platform in real time. The system uses the **front camera for lane detection** and the **left and right cameras for lateral correction relative to the lane edges**. Its main components include **front-camera bird's-eye preprocessing, color-thresholded lane extraction and clustering, Pure Pursuit steering, and PID speed control**.

## How Quanser Users Can Use This
- Use it for **teaching classical lane following on QCar**, from image preprocessing to steering control.
- Reuse the **front-camera bird's-eye preprocessing stack** as a low-latency baseline, then swap in lighter or alternative lane-detection methods.
- Use it as a **reference baseline on QCar 2** when comparing classical pipelines against more compute-heavy applied AI models, or other latency-sensitive perception stacks.
- Extract the **Pure Pursuit steering block** and connect it to another lane detector, path generator, or planner.
- Extend the stack toward **lane changes, intersections, dashed or faded lanes, and harder lighting conditions**.

## Experimental Setup
**Platform:** Quanser QCar  
**Sensors:** Front and side cameras 2D 350 CSI cameras  
**Environment:** Quanser Self-Driving Car Lab 

## Stack
**Tags:** QCar, MATLAB, Simulink, lane detection, DBSCAN, Pure Pursuit, PID, ARX, classical vision

## Links
**GitHub Repository:**  
https://github.com/khush-l/Lane-Centering-and-Following-Research_Project

**Paper:**  
https://github.com/khush-l/Lane-Centering-and-Following-Research_Project/blob/main/Paper_final_draft.pdf

**Sample video:**  
  https://github.com/khush-l/Lane-Centering-and-Following-Research_Project/tree/main/Videos\



## Authors
Khush Lalchandani · Aarav Paryemalani · Gideon White
