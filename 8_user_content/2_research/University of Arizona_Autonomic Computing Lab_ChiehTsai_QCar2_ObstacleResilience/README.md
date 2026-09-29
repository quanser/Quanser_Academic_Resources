# Obstacle Response and Recovery Under Software Attacks (Quanser QCar 2)

## Overview

This project studies **how software tampering can disrupt a vehicle's stopping decisions, and how to restore its intended behavior**. A changed distance threshold can make QCar 2 react too late even when an obstacle is detected correctly. Tis work combines YOLO perception and depth sensing with file integrity checks and backup recovery, with experiments in QLabs and on physical QCar 2. QCar users can build on these components to investigate **how detection and recovery timing affect stopping and mission completion**.

---

## How the Quanser Community Can Use This

- **Compare recovery strategies:** build matched scenarios for normal driving, tampering without protection, stopping after detection, and restoring a trusted configuration. Compare stopping behavior and mission completion.
- **Study detection timing:** vary the integrity check interval and vehicle speed. Measure detection delay and the distance traveled before recovery.
- **Handle unreliable perception:** add timestamps and fallback behavior for delayed or missing detections. Test whether the vehicle stops appropriately when perception becomes unavailable.
- **Connect digital twin and hardware experiments:** develop controlled tests in QLabs, then repeat validated scenarios on QCar 2. Compare distance estimates, stopping behavior, and recovery time.

---

## Experimental Setup

- **Platform:** QCar 2 and the QLabs QCar 2 digital twin.
- **Sensing and control:** RGB and depth images, vehicle pose and speed; obstacle distance rules, PI speed control, and Stanley steering.
- **Software and language:** Python, Quanser SDK, QLabs, OpenCV, and NumPy. Compatible YOLO model weights are required separately.

**Before use:** complete and validate the configuration recovery path, distance calibration, and stopping behavior in QLabs before physical trials.

---

## Stack / Tags

`QCar 2`, `Python`, `QLabs`, `YOLO`, `Cybersecurity`, `Software Integrity`, `Resilient Control`

---

## Links

- **Repository:** [intelligent-obstacle-resilience-av][repo]. Perception, vehicle control, and configuration tampering experiments.
- **Paper:** [Intelligent Obstacle Resilience in Autonomous Vehicles Under Security Threats][paper]. Chieh Tsai and Salim Hariri, IEEE CSCloud 2025.
- **Video:** [Author's explanation][video].

---

## Author Preferred Contact

For questions, bug reports, or feature requests, use [GitHub Issues][issues] on this project repository.

---

## Authors

Chieh Tsai; Salim Hariri.

Autonomic Computing Lab, University of Arizona. Developed by Chieh Tsai under the supervision of Prof. Salim Hariri.


[repo]: https://github.com/vegetableclean/intelligent-obstacle-resilience-av
[paper]: https://raw.githubusercontent.com/vegetableclean/vegetableclean.github.io/main/assets/pdf/cscloud.pdf
[issues]: https://github.com/vegetableclean/intelligent-obstacle-resilience-av/issues
[video]: https://drive.google.com/file/d/1UJIRGdNgQHYSJj645q2r6ike3_ldHu72/view
