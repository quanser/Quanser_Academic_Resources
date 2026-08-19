# QA2C (Quanser Aero 2)

## Overview

QA2C is a research framework for **homomorphic encryption control** on the **Quanser Aero 2**. It transforms full state feedback and dynamic controllers into quantized and encrypted forms, then runs the controller across a split setup: **Windows plant interface** using the Quanser Aero 2 Python API and a **Linux or WSL controller** connected through **TCP/IP**.

The framework supports nominal, quantized, and encrypted controller versions using **OpenFHE Python** and **Microsoft SEAL**.

---

## How the Quanser Community Can Use This

- Compare nominal, quantized, and encrypted control pipelines on the same Aero 2 task.
- Benchmark OpenFHE Python and Microsoft SEAL using control latency, tracking performance, and stability.
- Study encrypted full state feedback, observer based control, and integral control with transformed ARX models.
- Reproduce the workflow in Quanser Interactive Labs before moving to the physical Aero 2.
- Modify the quantization, scaling, controller gains, or encryption parameters for new secure control experiments.
- Extend the same architecture to other low dimensional Quanser systems.

---

## Experimental Setup

- **Platform:** Quanser Aero 2
- **Architecture:** Windows plant interface + TCP/IP + Linux or WSL controller

---

## Stack / Tags

`Python`, `C++`, `TCP/IP`, `OpenFHE`, `Microsoft SEAL`, `Homomorphic Encryption`, `Encrypted Control`, `Cyber Physical Security`, `Aero 2`

---

## Links

- **GitHub Repository:**  
https://github.com/RFA0608/QA2C
- **Quanser Interactive Labs Demo:**  
https://youtu.be/gvt1yL_Wo3I

---

## Authors
jeongmingyu@cdslst.kr (Mingyu Jeong)  
leesangwon@cdslst.kr (Sangwon Lee)  
leedonghyun@cdslst.kr (Donghyun Lee)