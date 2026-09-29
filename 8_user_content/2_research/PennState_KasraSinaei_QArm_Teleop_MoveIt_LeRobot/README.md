# Teleoperation, Motion Planning, and Demonstration Recording (Quanser QArm)

## Overview

`qarm_teleop` gives QArm users **tools to plan motions, control the arm through an SO-101 leader, and collect demonstrations for imitation learning**. Built on Quanser's ROS 2 examples, it adds **MoveIt 2** integration and a **LeRobot** recorder for saving camera images, measured joint states, and commanded actions.

Researchers can develop planned motions and collect their own demonstrations while reusing the existing robot interface. **Policy training and autonomous policy execution are separate extensions, not included features.**

---

## How the Quanser Community Can Use This

- **Collect manipulation demonstrations:** adapt the recorder for tasks such as object transfer or sorting, saving camera images, measured states, and actions in LeRobot format.
- **Develop imitation learning policies:** use the collected demonstrations in a compatible training workflow. Compare task success with different numbers of demonstrations or one versus two camera views.
- **Explore motion planning:** use the MoveIt bridge to send planned joint trajectories to QArm. Compare planned and measured motion for different position goals and speed settings.
- **Improve demonstration quality:** adjust the leader mapping and camera placement, then study tracking error, recording delay, and task repeatability.

---

## Experimental Setup

- **Platform:** Quanser QArm; SO-101 leader for teleoperation
- **Sensors:** QArm RealSense gripper camera, an external RealSense camera
- **Software and language:** Python, ROS 2, Quanser SDK, MoveIt 2, LeRobot, OpenCV, and RealSense libraries on Ubuntu.

---

## Stack / Tags

`QArm`, `Python`, `ROS 2`, `MoveIt 2`, `SO-101`, `Teleoperation`, `LeRobot`, `Imitation Learning`

---

## Links

- **Repository:** [qarm_teleop][repo]. ROS 2 packages, robot description, teleoperation, and MoveIt configuration.

---

## Author

Kasra Sinaei

Electrical Engineering, Pennsylvania State University.

[repo]: https://github.com/Kassra-sinaei/qarm_teleop
