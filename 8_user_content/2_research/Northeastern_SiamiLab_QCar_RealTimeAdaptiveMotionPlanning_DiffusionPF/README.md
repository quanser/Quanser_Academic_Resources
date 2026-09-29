# Real-Time Adaptive Motion Planning via Diffusion + Potential Fields

![RAMP repository overview screenshot](https://private-user-images.githubusercontent.com/50802328/462830839-ad1f25e2-40ca-4d0e-ac7e-5d7b37ca8544.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Njk1NDc2OTgsIm5iZiI6MTc2OTU0NzM5OCwicGF0aCI6Ii81MDgwMjMyOC80NjI4MzA4MzktYWQxZjI1ZTItNDBjYS00ZDBlLWFjN2UtNWQ3YjM3Y2E4NTQ0LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjAxMjclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwMTI3VDIwNTYzOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWYwOGU0NmMwN2Q4NWQ5ZWQ4ZjA2Mjg3MWUzYmVkZWY1MjdjNmUwMzI2NDU0NjNlMmE1OTU1MjlkZDFjZGQwMzMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.tXwt584whhxxCUDODWtvlvaD-BC6u8h1sdXU-6ouz7w)
<!-- Image source: wondmgezahu/RAMP repository (README), branch: main. -->

## Overview

RAMP is a real-time planner that generates trajectories directly from **obstacle point clouds**. It combines:

- a **point-cloud guided, energy-based diffusion** planner (global trajectory proposals), with  
- **potential-field refinement** (local last-meter collision avoidance),

and supports **online refinement** when a moving threat (a “pursuer”) gets close.

**Catch:** it is a hybrid “learned global planner + reactive safety correction” approach designed for fast replanning.

---

## How the Quanser Community Can Use This

- **Fast start for teaching/research:** run the repo’s QCar demo, then change one knob (obstacles, sensor, safety distance, speed).
- **Add a pursuer:** use a second QCar as the moving “threat” and test replanning.
- **Make your own maps:** auto-generate obstacle layouts + start/goal pairs for repeatable tests.
- **Benchmark planners:** compare APF, RRT/BIT*, optimization, RL, and diffusion with the same metrics.
- **Increase difficulty easily:** add clutter, moving obstacles, uncertainty, tighter limits.
- **Extend projects:** swap sensors, tune the cost (smoother/safer/faster), or go multi-agent.

---

## Experimental Setup

- **Platform:** QCar1
- **Task:** obstacle avoidance and pursuit–evasion planning from point-cloud obstacles
- **Data:** synthetic obstacle layouts + start/goal pairs + diverse trajectories (dataset generation scripts)


---

## Stack / Tags

**Tags:** `QCar` `Motion planning` `Point clouds` `Diffusion` `Potential fields` `Pursuit–evasion`

---

## Links

- **GitHub Repository:**  
  https://github.com/wondmgezahu/RAMP

- **Paper (arXiv):**  
  https://arxiv.org/abs/2507.09383

---

## Authors

Wondmgezahu Teshome · Kian Behzad · Octavia Camps · Michael Everett · Milad Siami · Mario Sznaier
