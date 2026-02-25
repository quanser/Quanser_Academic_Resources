# qarm-hack (Quanser QArm, Python + PyBullet)

## Overview
`qarm-hack` provides a simulation-to-hardware control path for the **Quanser QArm** using a single joint-space API. It runs the QArm in a **PyBullet** physics simulation (URDF + meshes, with a viewer) and is structured to later switch to **real QArm hardware** via a `RealQArm` backend once the Quanser SDK integration is available.


---

## How the Quanser Community Can Use This
- **Compare QArm simulation stacks for teaching and research:** use this PyBullet option alongside **QLabs (Unreal Engine)** and **ROS 2 + Gazebo** ([RobinHerrmann_gazebo_qarm_sim_QArm_ROS2_Gazebo_Sim](../RobinHerrmann_gazebo_qarm_sim_QArm_ROS2_Gazebo_Sim)) to evaluate which workflow fits best.
- **Run performance and infrastructure experiments:** compare setup friction, headless vs GUI runtime, stability, and reproducibility across QLabs, Gazebo, and PyBullet using a shared pick-and-place style task.
- **Use PyBullet when you want a robotics-first physics engine:** prototype kinematics/IK strategies, gripper behaviors, and collision-aware manipulation in a fast Python loop.
- **Prototype new applications on top of the existing scene and API:** extend tasks beyond hoops by adding new objects, rules, constraints, and helpers without changing the core simulator code.
- **Support a sim-to-real workflow with the same interface:** keep student or research code stable while swapping the backend from simulation to hardware when available.

---

## Experimental Setup
- **Platform:** QArm
- **Software:** Quasner SDK
- **Physics:** PyBullet
- **Model:** QArm URDF + mesh resources
- **Viewer:** Panda3D-based viewport (PyBullet GUI can be enabled for debugging)

---

## Stack / Tags
`Python`, `PyBullet`, `URDF`, `Manipulation`, `Joint-space Control`, `Sim-to-Real`

---

## Links
- **GitHub Repository:** 
https://github.com/aj-floater/qarm-hack
---

## Authors
Archie James (@aj-floater), Thierry (@Thierryonre), Tara Mulhall (@tara257), UoM RoboSoc (@UoM-RoboSoc)