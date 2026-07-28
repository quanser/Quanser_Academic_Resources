# QCar2 Platooning in QLabs

## Overview
This repository explores **multi-vehicle platooning with Quanser QCar2** in **QLabs**, with the longer-term goal of supporting the same codebase on physical vehicles as well. It studies how a fleet of small autonomous cars can maintain safe spacing, share motion information, and behave as a coordinated convoy instead of as independent vehicles. The current working baseline is a **headway-based follower controller** running in a **50 Hz closed loop** with **LiDAR, GPS, and IMU** sensing, while the next research step is a more cooperative **distributed controller** that uses richer inter-vehicle communication and topology-aware coordination. The project is especially valuable as a compact research platform for **platooning, convoy control, communication topology studies, and multi-agent vehicle coordination**.

---

## How Quanser Users Can Use This Work

- Use it as a **QCar2 platooning baseline** for convoy and gap-keeping experiments.
- Compare different **communication topologies** such as predecessor-following, all-to-all, or local-neighbor coordination.
- Build on the working **headway controller** before extending toward distributed or cooperative control.
- Reuse the shared **simulation / physical-hardware structure** as a starting point for moving from QLabs to real QCar2 tests.

---

## Experimental Setup

- **Platform:** QCar2
- **Environment:** QLabs
- **Sensors:** LiDAR, GPS, IMU
---

## Stack

**Tags:** `QCar2` `QLabs` `Platooning` `Convoy Control` `LiDAR` `GPS` `IMU` `Headway Control` `Distributed Control` `Python` `Telemetry Logging`

---

## Links

- **GitHub Repository:**  
https://github.com/mengshengya/QCar2Platoon_QLab
- **Project Page:** 
https://artismo-website.vercel.app/results.php?id=platoon-applications-platform-testing&lang=en

---

## Authors

Shengya Meng