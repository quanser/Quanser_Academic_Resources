# Multi-Agent Research Examples

This folder contains multi-vehicle and multi-robot examples built on Quanser Interactive Labs and the `qvl` interface. The examples demonstrate how to spawn multiple agents in a shared QLabs world, configure a custom environment, and run separate control loops or perception-driven behaviors at the same time.

## Overview

The multi-agent examples in this directory are intended for research and prototyping workflows that involve:

- simultaneous multi-robot spawning
- multi-instance control logic
- custom map or environment setup
- robot coordination within a single QLabs session
- MATLAB/Simulink or Python-based control workflows

## Included Examples

| Example | Platform | Environment | Description |
| --- | --- | --- | --- |
| [QCar2_multi-vehicle_control](./QCar2_multi-vehicle_control) | QCar 2 | Cityscape / Cityscape Lite | Spawns two QCar 2 vehicles and runs two independent control instances in the same world. |
| [QBP_multi-line_following](./QBP_multi-line_following) | QBot Platform | Open Warehouse | Spawns multiple QBot Platforms and demonstrates line following using a camera-based perception workflow. |

### QCar2_multi-vehicle_control

This example creates a world with two QCar 2 vehicles and demonstrates how to run multiple vehicle controllers in a single QLabs session.

Key points:

- Uses the `MultiAgent` API from `qvl.multi_agent`
- Spawns vehicles in either Cityscape or Cityscape Lite
- Runs two separate controller scripts for each vehicle
- Shows how to build a multi-vehicle testbed for SDCS research and experimentation

Files in this folder:

- [QCar2_multi-vehicle_control/initCars.py](./QCar2_multi-vehicle_control/initCars.py) — spawns both vehicles in the QLabs scene
- [QCar2_multi-vehicle_control/vehicle_control.py](./QCar2_multi-vehicle_control/vehicle_control.py) — first vehicle controller
- [QCar2_multi-vehicle_control/vehicle_control2.py](./QCar2_multi-vehicle_control/vehicle_control2.py) — second vehicle controller
- [QCar2_multi-vehicle_control/run.bat](./QCar2_multi-vehicle_control/run.bat) — convenience launcher for the example

Typical workflow:

1. Open QLabs in the appropriate Cityscape environment.
2. Run [QCar2_multi-vehicle_control/initCars.py](./QCar2_multi-vehicle_control/initCars.py) to spawn the vehicles.
3. Run [QCar2_multi-vehicle_control/vehicle_control.py](./QCar2_multi-vehicle_control/vehicle_control.py) and [QCar2_multi-vehicle_control/vehicle_control2.py](./QCar2_multi-vehicle_control/vehicle_control2.py) in separate terminals.
4. When prompted, select QCar 2 as the robot type.

### QBP_multi-line_following

This example creates a multi-agent QBot Platform configuration in the Open Warehouse environment and uses line-following logic to drive multiple robots.

Key points:

- Supports both MATLAB/Simulink and Python setup workflows
- Uses a multi-agent map configuration in an Open Warehouse environment
- Integrates a line-following application with downward-facing camera input
- Uses a Logitech F710 gamepad to arm the virtual QBot Platforms and enable motion

Files in this folder:

- [QBP_multi-line_following/setup_python.py](./QBP_multi-line_following/setup_python.py) — Python setup script for spawning the multi-agent environment
- [QBP_multi-line_following/setup_matlab.m](./QBP_multi-line_following/setup_matlab.m) — MATLAB workspace setup script
- [QBP_multi-line_following/line_following_2023a.slx](./QBP_multi-line_following/line_following_2023a.slx) — Simulink model used for the multi-agent line-following workflow

Typical workflow:

1. Open the relevant QLabs environment.
2. Run the setup script for either Python or MATLAB.
3. Launch the Simulink model or controller script for the QBot Platforms.
4. Use the Logitech F710 gamepad to arm the robots and enable their motion.
5. The downward-facing camera on each platform is used for line detection and line-following behavior.

## Folder Structure

```text
5_research/
└── multi_agent/
    ├── README.md
    ├── testingMultiAgent.py
    ├── QCar2_multi-vehicle_control/
    │   ├── initCars.py
    │   ├── vehicle_control.py
    │   ├── vehicle_control2.py
    │   ├── run.bat
    │   ├── cityscape.png
    │   └── SDCS_RoadMap_RightHandTraffic.png
    └── QBP_multi-line_following/
        ├── setup_python.py
        ├── setup_matlab.m
        ├── line_following_2023a.slx
        └── line_following_2023a.slx.r2023a
```

## Prerequisites

Before running these examples, confirm that the following are available:

- Quanser Interactive Labs is installed and running
- The proper QLabs environment is open for the selected example
- The QLabs Python or MATLAB library (`qvl`) is available in the active development environment
- MATLAB/Simulink and QUARC are available for the QBot line-following example
- The repository setup steps in [1_setup](../../1_setup) have been completed

For additional background, review the repository setup guides in [1_setup](../../1_setup), [2_quick_start_guides](../../2_quick_start_guides), and [3_user_manuals](../../3_user_manuals).

## Notes

- [testingMultiAgent.py](./testingMultiAgent.py) is a useful validation script for checking MultiAgent spawning and robot metadata.
- These examples are meant to be used as research templates and can be adapted for custom multi-agent experiments.
- The environment and robot placement values in each script are specific to the demo configuration and may need adjustment for your installation or map.

## Related Resources

- [5_research/README.md](../README.md)
- [1_setup](../../1_setup)
- [2_quick_start_guides](../../2_quick_start_guides)
- [3_user_manuals](../../3_user_manuals)

---

This directory provides a compact starting point for multi-agent experimentation with QCar 2 and QBot Platform systems in Quanser QLabs environments.
