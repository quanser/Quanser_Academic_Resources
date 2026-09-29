# AutoNavRL: Reinforcement Learning Navigation (Quanser QBot)

## Overview

`AutoNavRL` uses **reinforcement learning to navigate to a target position and heading while avoiding multiple static and dynamic obstacles.** A TD3 policy learns in IRSim to turn lidar readings and goal information into linear and angular velocity commands. The project shares training and evaluation code, saved policies, and ROS deployment scripts. The author reports deploying a trained policy on a physical Quanser QBot.

One practical feature of the [QBot interface][boundary] is adding **virtual arena boundaries to real lidar readings**, making the observations resemble the bounded training environment. Researchers can start with the saved policy, modify how navigation is learned, and investigate the changes needed to transfer it to their own robot setup.

---

## How the Quanser Community Can Use This

- **Teach reward design:** use the saved TD3 policy as a starting point, then change rewards for goal progress, final heading, and obstacle clearance. Compare the resulting paths and behavior (Robotics or Reinforcement Learning).
- **Improve obstacle awareness:** compare different lidar resolutions or add a short history of scans. Test whether these changes help with moving obstacles and unfamiliar layouts.
- **Compare learning algorithms:** adapt the training and evaluation scripts for SAC or PPO, then compare with TD3 using equal training budgets and the same test scenarios. Their saved checkpoints alone are not a matched comparison.
- **Study transfer to QBot:** investigate virtual arena boundaries and sensitivity to localization error. Match scan processing and command timing before evaluating a policy on hardware.

Compare **success and collision rates, travel time, path length, and final heading error**, using fixed test cases separate from training.

---

## Experimental Setup

- **Platform:** differential drive robot in IRSim; physical Quanser QBot Platform.
- **Software and language:** Python 3.10, IRSim, Stable-Baselines3, PyTorch, and Gym; ROS for hardware deployment.
- **Sensors and signals:** lidar, goal distance and direction, final heading error, and previous velocity commands; outputs are linear and angular velocity commands.
- **Training environment:** a 6 x 6 m arena with stationary and moving obstacles.
- **Saved policies:** TD3, SAC, and PPO checkpoints. The supplied training, evaluation, and deployment scripts use TD3.
---

## Stack / Tags

`QBot`, `Python`, `Reinforcement Learning`, `TD3`, `ROS`, `Lidar`, `Robot Navigation`

---

## Links

- **Repository:** [AutoNavRL source code and project description][repo].

---

## Author

[Harsh Mahesheka][author]. Developed as part of the author's master's thesis.

Indian Institute of Technology, Varanasi.

**Email:** [harsh.mahesheka.eee20@iitbhu.ac.in](mailto:harsh.mahesheka.eee20@iitbhu.ac.in)

**Website:** [Personal homepage][homepage].

[repo]: https://github.com/harshmahesheka/AutoNavRL
[author]: https://github.com/harshmahesheka
[boundary]: https://github.com/harshmahesheka/AutoNavRL/blob/master/ros-deployment/real_env.py
[homepage]: https://harshmahesheka.github.io/
