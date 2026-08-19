# QCar TouchDrive: Mobile Web Teleoperation for Physical and Virtual QCar

## Overview
`QCar TouchDrive` is a **mobile web teleoperation interface** for the **Quanser QCar**. It lets a user drive the car from a phone through a browser-based dual-joystick UI, while a Python server on the QCar host sends real-time steering and throttle commands to either the **physical QCar** or the **QLabs virtual lab**. In addition to manual driving, it provides live telemetry, basic safety controls, and CSV logging, making it a practical tool for demos, remote operation, and manual data collection.

---

## How the Quanser Community Can Use This
- A simple **phone-based driving interface** for QCar without a separate hardware controller.
- A practical setup for **live demos**, classroom activities, and remote teleoperation.
- A shared interface for both **physical QCar** and **QLabs simulation**.
- A lightweight way to collect **manual driving data** for calibration, system ID, or ML workflows.
- A useful example of combining **web UI + Python server + Quanser SDK** into one clean control tool.

---

## Experimental Setup
- **Target platform:** QCar; QLabs Virtual Lab
- **Software:** Quanser SDK
- **Network:** Local LAN or **Tailscale** for secure remote access
- **Communication:** WebSocket between phone browser and host server

---

## Stack / Tags
`Python`, `WebSocket`, `Tailscale`, `Teleoperation`, `Mobile Control`, `QCar`, `QLabs`, `Data Logging`, `Web UI`

---

## Links
- **GitHub Repository:**  
https://github.com/vegetableclean/qcar-touchdrive

---

## Author Preferred Contact

For questions, bug reports, or feature requests, please use **[GitHub Issues](https://github.com/vegetableclean/qcar-touchdrive/issues)** on the project repository.

---

## Author
Developed by Chieh Tsai under the supervision of Prof. Salim Hariri, Autonomic Computing Lab, University of Arizona.
