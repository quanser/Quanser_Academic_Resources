# QQS3C (Quanser Qube Servo 3)

## Overview
QQS3C is a research framework for **homomorphic-encryption (HE) control** on the **Quanser Qube Servo 3**. It rewrites controllers into **HE-friendly forms** (plus quantized variants) and runs the controller computation across a split setup: **Windows plant/interface** (Quanser Python API) ↔ **Linux/WSL controller** via **TCP/IP**.

---

## How the Quanser Community Can Use This
- Benchmark controller forms (observer / ARX / integer-matrix) in **plain vs quantized vs encrypted** pipelines.
- Benchmark HE ecosystems (**SEAL C++**, **OpenFHE Python**, **lattigo/CDSL Go**) on the same control task and compare latency vs stability.
- Re-run the end-to-end flow quickly (start plant on Windows, start controller on WSL) to reproduce baseline demos.
- Extend as new research by changing **quantization/scaling** and re-testing with the same pipeline for apples-to-apples results.
- Port the architecture to other **low-dimensional** Quanser plants (encoder/IMU signals);

---

## Experimental Setup
- **Platform:** Quanser Qube Servo 3
- **Architecture:** Windows plant/interface + TCP/IP + Linux/WSL controller

---

## Stack / Tags
`Python`, `TCP/IP`, `C++ (SEAL)`, `Go (lattigo/CDSL)`, `Homomorphic Encryption`, `Cyber-physical security`, `Encrypted Control`, `Qube Servo 3`

---

## Links
* **GitHub Repository:** 
https://github.com/RFA0608/QQS3C

---

## Authors
jeongmingyu@cdslst.kr (Mingyu Jeong)  
leesangwon@cdslst.kr (Sangwon Lee)  
leedonghyun@cdslst.kr (Donghyun Lee)