# QBot Platform ROS 2 Packages

QBot Platform ROS 2 packages now lives in the [`qbot_hardware`](<https://github.com/quanser/qbot_hardware.git>) and [`qbot_rl_deploy`](<[link-to-qbot_rl_deploy-repo](https://github.com/quanser/qbot_rl_deploy.git)>) repos. 

| Repo | Contains |
|---|---|
| `qbot_hardware` | `qbot_hardware` (drivers) and `qbot_localization` (scan-match / EKF localization) |
| `qbot_rl_deploy` | `qbot_rl_deploy` (RL policy deployment nodes) and `qbot_rl_interfaces` (msg/action definitions) |

`qbot_rl_deploy` depends on `qbot_hardware` at runtime (sensor, pose, and reset-service topics). See each repo's own README for full details on nodes, topics, parameters, and launch files.

## Connecting to the QBot Platform

Before building or running anything, make sure you can connect to the QBot Platform's onboard Jetson. See the [**User Manual – Connectivity**](</../../3_user_manuals/qbot_platform/user_manual_connectivity.pdf>) guide for network setup and connection instructions.

## Getting the Code

There are two scenarios, depending on whether the QBot's onboard Jetson has internet access. Each command block below is labeled with where to run it.
 
### Scenario A — Jetson has internet access
**Run on your computer**, ssh into QBot Platform:
 
```bash
ssh nvidia@<QBOT_IP_ADDRESS>
```
 
**Run on QBot (inside the SSH session):**
 
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/quanser/qbot_hardware.git
git clone https://github.com/quanser/qbot_rl_deploy.git
```

### Scenario B — Jetson has no internet access

**On your computer**, create a folder named `ros2_ws`, and inside it a folder named `src` (e.g. using File Explorer, or your terminal of choice).
 
**Run on your computer**, inside `ros2_ws/src`, clone both repos:
 
```bash
git clone https://github.com/quanser/qbot_hardware.git
git clone https://github.com/quanser/qbot_rl_deploy.git
```
 
Transfer the cloned `ros2_ws` folder onto the QBot Platform. See [**User Manual – Connectivity**](</../../3_user_manuals/qbot_platform/user_manual_connectivity.pdf>) for file transfer instructions
 
**Run on your computer**, connect to QBot Platform:
 
```bash
ssh nvidia@<QBOT_IP_ADDRESS>
```
**Run on QBot (inside the SSH session)**, confirm the file transfer:

```bash
ls ~/ros2_ws/src
```

## Build

**Run on QBot (inside the SSH session)**, source ROS 2 Humble, then build from the `ros2_ws/` root:

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws/src
colcon build --symlink-install
source install/setup.bash
```

Instructions on how run the nodes and launch files are in each repo's README.

## License

Apache-2.0
