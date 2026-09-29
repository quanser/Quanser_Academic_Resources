# Latency and Jitter in Pendulum Control (Quanser Qube-Servo 3)

## Overview

`LatencyPendulumControl` studies **how delayed measurements affect pendulum balance**. It compares **LQR, LQR with a Kalman filter, and LQR with a Smith predictor** on a physical Qube-Servo 3, with configurable feedback delay and jitter.

The project shares **C++ control code, Python design and analysis tools, and recorded experiments** from Mahmoud Ayoub's master's [thesis][thesis]. Educators can use these resources to teach state estimation and distributed control, or build assignments around the recordings without requiring hardware.

---

## How the Quanser Community Can Use This

- **Teach delay effects:** compare balancing with and without added feedback delay. Connect sampling, measurement age, and stability in a Control Systems lab.
- **Explore estimation and prediction:** change Kalman noise settings or predictor model parameters and investigate their effect on balance and motor commands (Advanced Controls).
- **Use recordings in coursework:** plot logged angles, voltages, and timing with the Python tools, then identify when balance is lost. No hardware is needed for this activity.
- **Build a distributed control project:** adapt the hardware and controller processes to run on separate computers, then compare measured network timing with the injected delay.

For comparisons, use matched effective gains and evaluation windows, and check the realized delay and jitter rather than only the requested settings.

---

## Experimental Setup

- **Platform:** Quanser Qube-Servo 3 rotary pendulum
- **Software and language:** C++ and Quanser HIL SDK; Python with NumPy, SciPy, pandas, and Matplotlib
- **Host and communication:** Raspberry Pi 3 Model B+ running Linux, with a nominal 200 Hz loop. The reported experiments run both processes on the same Pi using UDP; feedback delay is introduced in software.

---

## Stack / Tags

`Qube-Servo 3`, `C++`, `Python`, `LQR`, `State Estimation`, `Networked Control`, `Control Education`

---

## Links

- **Repository:** [LatencyPendulumControl][repo]. Control code, design scripts, and analysis tools; MIT license.
- **Thesis:** [Comparing the Effects of Latency and Jitter in Distributed Furuta Pendulum Control][thesis]. Mahmoud Ayoub, 2026. [Full text PDF][pdf].
- **Experimental recordings:** [CSV logs and analysis resources][recordings].

---

## Author

Mahmoud Ayoub.

Mälardalen University, Department of Computer Science & Engineering, Sweden.

**Supervisor:** Anna Friebe.

[repo]: https://github.com/annafriebe/LatencyPendulumControl
[thesis]: https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A2071263
[pdf]: https://www.diva-portal.org/smash/get/diva2:2071263/FULLTEXT01.pdf
[recordings]: https://github.com/annafriebe/LatencyPendulumControl/tree/main/CollectedData
