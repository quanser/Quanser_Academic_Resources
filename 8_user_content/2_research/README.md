<div align="center" style="margin-bottom:24px;">
  <div style="width:100%; max-width:1300px; aspect-ratio: 2 / 1; overflow:hidden; border-radius:9px;">
    <img img src="../images/header_user_generated_content_research.jpg"
         alt="Header"
         style="width:100%; height:100%; object-fit:cover; display:block;" >
  </div>
</div>



## Research

![Category](https://img.shields.io/badge/category-research-1f6feb?style=flat-square)
![Platforms](https://img.shields.io/badge/platforms-QCar%20%7C%20QDrone%20%7C%20Qube%20%7C%20Aero%20%7C%20QLabs-8250df?style=flat-square)
![Areas](https://img.shields.io/badge/areas-RL%20%7C%20Planning%20%7C%20SLAM%20%7C%20VIO%20%7C%20MPC%20%7C%20SysID%20%7C%20Edge%20AI%20%7C%20VLM%20%7C%20Secure%20Ctrl-ffb000?style=flat-square)

Quanser platforms are used by researchers in 90+ countries, with 300+ papers published each year. This repository curates a growing set of those works and artifacts (papers, code, datasets) so you can find and build on them faster.

Use the index to browse by platform and research area. For example: Reinforcement Learning (RL) on QCar, secure control on Qube, SLAM/map fusion, planning, edge–cloud AI in QLabs, or system identification on QDrone.

> **Note on credit:** Each entry links to the original authors’ repository (and paper/dataset when available). All credit remains with the creators.


---

### Research index

| Institution | Lab | Author(s) | Project title | Platform | Domain | Approach |
|---|---|---|---|---|---|---|
| University of Ottawa | SCVIC | Murat Arda Onsu; Poonam Lohan; Burak Kantarci; Aisha Syed; Matthew Andrews; Sean Kennedy | [Multimodal LLM Traffic Monitoring (QLabs dataset)](University%20of%20Ottawa_SCVIC_QLabsVirtualQCar_MultimodalTrafficMonitoring_Dataset/)| QLabs | VLM; Perception | Dataset + pipeline: instance segmentation first, then VLM fine-tuning for traffic Q&A and incident awareness. |
| University of Ottawa | SCVIC | Murat Arda Onsu; Poonam Lohan; Burak Kantarci; Aisha Syed; Matthew Andrews; Sean Kennedy | [Semantic Edge–Cloud Traffic Surveillance (QLabs dataset)](University%20of%20Ottawa_SCVIC_QLabsVirtualQCar_SemanticEdgeCloudTrafficSurveillance_Dataset) | QLabs | Edge AI; VLM | Edge sends compact semantics (ViT embeddings) instead of full frames; cloud reconstructs crops for LLM-based captions/Q&A under link constraints. |
| University of Windsor | N/A | Sooraj Sunil; Saeed Mozaffari; Rajmeet Singh; Behnam Shahrrava; Shahpour Alirezaee | [Collaborative SLAM Map Fusion](University%20of%20Windsor_SoorajSunil_QCar_LiDAR_CooperativeSLAM_Params) | QCar | SLAM | Feature-based registration + Bayesian fusion to merge heterogeneous occupancy grids; companion repo provides real QCar LiDAR scans. |
| Uppsala University | N/A | Sam Farkhooi | [Embedded MPC for QUBE-Servo 2](Uppsala%20university_SamFarkhooi_QubeServo2_EmbeddedMPC_InvertedPendulumSwingUpConstraints) | Qube Servo 2 | MPC | Energy-based swing-up followed by constrained MPC stabilization, implemented for embedded real-time execution (ESP32 + QFLEX 2). |
| UT Austin | N/A | Yujing Zhou; Zejiang Wang; Junmin Wang | [Illumination-Resilient Lane Detection (Newton-ES)](UT%20Austin_BryantZhou_QCar_IlluminationResilientLaneDetection_NewtonES) | QCar | Perception | Online self-tuning of HSV thresholds via Newton-based extremum seeking for lane detection robust to lighting changes. |
| UT Austin | N/A | Perry A. Scott; Bryant Zhou | [Autonomous Driving with RL (DDPG)](UT%20Austin_PerryScott_QCar_ReinforcementLearning_DDPG) | QCar | RL | Practical baseline for actor–critic continuous control on QCar-scale vehicles, trained offline from recorded experience logs. |
| Zhejiang University | N/A | Xinwen Zhu; Zihao Li; Yuxuan Jiang; Jiazhen Xu; Jie Wang; Xuyang Bai | [Real-Time V2V Cooperative Control (intersection)](Zhejiang%20university_QCar_DistributedV2VCooperativeControl) | QCar | Multi-agent | Multi-QCar coordination using etcd as a shared “environment pool,” with lease scheduling and robustness via Raft leader failover. |
| Northeastern University | Siami Lab | Kian Behzad; Maral Mordad; Rojin Zandi; Milad Siami | [Wi-Fi CSI Object Detection (RF sensing)](Northeastern_SiamiLab_QCar_WiFiCSIObjectDetection) | QCar | RF sensing | Two QCars using standard Wi-Fi hardware perform non-line-of-sight object detection via Channel State Information (CSI). By driving around a closed container and analyzing reflections, the system classifies whether the box is empty or filled, treating QCar as a mobile RF sensing platform. |
| Clemson University | N/A | Ameya Salvi; John Coleman; Jake Buzhardt; Venkat Krovi; Phanindra Tallapragada | [Vertical Stabilization on Bumpy Terrain (DDPG)](Clemson_KroviTallapragada_QCar_BumpyTerrain_VerticalStabilization_RL/) | QCar | RL | Terrain-aware speed control learns to reduce vertical acceleration (bounce) while balancing comfort and progress. |
| Columbus State University | N/A | Muhammad Talha Ejaz | [Edge Vision: VGG16 vs MobileNet (edge AI)](Columbus%20state_MuhammadTalhaEjaz_QCar_EdgeVision_VGG16_vs_MobileNet) | QCar | Edge AI | Transfer-learning comparison of a heavier vs lightweight CNN for perception under edge compute constraints, with an included dataset. |
| Khalifa University | ARIC | Abdulla Ayyad; Mohamad Chehadeh; Mohammad I. Awad; Yahya Zweiri | [Real-Time System Identification (DNN + MRFT)](Khalifa%20university_ARIC_QDrone_QDrone_RealTimeSystemID_DNN) | QDrone | SysID | Identify-then-tune workflow: MRFT induces oscillation, one cycle is classified against a model library, then gains are looked up and applied. |
| Khalifa University | ARIC | Abdel Gafoor Haddad; Igor Boiko; Yahya Zweiri | [RL Generalization via Homogeneity Transforms](Khalifa%20university_ARIC_QDrone_RLGeneralization_HomogeneityTransforms) | QDrone | RL | A nominal RL policy is wrapped with physics-derived scaling to stay effective across parameter variations (e.g., cable length changes). |
| Northeastern University | Siami Lab | Reza Vafaee; Kian Behzad; Milad Siami; Luca Carlone; Ali Jadbabaie | [Non-submodular Visual Attention for Visual–Inertial Odometry](Northeastern_SiamiLab_QCar_NonsubmodularVisualAttention) | QCar | Visual–Inertial Odometry. | Selects κ “best” features per frame to balance Visual–Inertial Odometry. accuracy vs runtime; includes a QCar dataset (EuRoC format). |
| Northeastern University | N/A | Wondmgezahu Teshome; Kian Behzad; Octavia Camps; Michael Everett; Milad Siami; Mario Sznaier | [RAMP: Diffusion + Potential Fields (planning)](Northeastern_SiamiLab_QCar_RealTimeAdaptiveMotionPlanning_DiffusionPF) | QCar | Planning | Hybrid planner: diffusion proposes global trajectories; potential fields provide fast local safety refinement for replanning. |
| Norwegian University of Science & Technology| Engineering Cybernetics | Finn Ferdinand Schjøll Sandvand | [Orbital Stabilization Control (nonlinear/robust)](Norwegian%20Sci-Tech%20university_EngineeringCybernetics_QuanserAero_OrbitalStabilization_Robustification) | Quanser Aero | Robust control | Complete Aero workflow including modeling, verification, observers, identified coefficients, and experimental demonstrations. |
| Queen’s University | N/A | Hudson M. S. Bruno; Ketly M. Cabral; Esther L. Colombini; Sidney N. Givigi | [Deep Learning VO under Degradation](Queens%20university_QUARRG_QCar_DeepLearningVO_ChallengingScenarios) | QCar | VO | RGB dataset with Vicon ground truth; evaluates deep VO robustness under emulated exposure and lens-failure modes. |
| SeoulTech | CDSL | Mingyu Jeong; Sangwon Lee; Donghyun Lee | [Qube Servo 3: Homomorphic Encrypted Control (cybersecurity)](SeoulTech_CDSL_QubeServo3_HomomorphicEncryptedControl) | Qube Servo 3 | Secure Ctrl | HE-friendly controller rewrites + split Windows plant ↔ WSL/Linux controller; compare plain vs quantized vs encrypted pipelines. |
| Sivas Bilim ve Teknoloji Üniversitesi | N/A | Asaf Sayıl | [LNN: Learning-based Control Pipeline (benchmarking)](Sivas%20BilimVe%20Teknoloji%20universitesi_RFL_CfCvsLQR_NeuralControlBenchmark) | Rotary Flexible Link (RFL) | Learning control | End-to-end workflow: hardware logging → dataset → training → deployment/evaluation, with an LQR baseline for comparison. |
| University of Alabama in Huntsville | N/A | Samuel Newport | [NASMC on Quanser Aero (adaptive + SMC)](University%20of%20Alabama%20in%20Huntsville_RoboticsControlsLab_QuanserAero_NASMC_AdaptiveSlidingMode_Sim) | Quanser Aero | Adaptive control | MATLAB/Simulink NASMC models for pitch–yaw helicopter; compare robustness vs baseline controllers under uncertainty. |
| N/A | N/A | Robin Herrmann | [Gazebo QArm Simulation (ROS 2 + Gazebo, RL-ready)](RobinHerrmann_gazebo_qarm_sim_QArm_ROS2_Gazebo_Sim/) | QArm | Simulation; RL | ROS 2 Humble + Gazebo 11 QArm model using ros2_control; designed to support RL via a Gym-style QArmEnv interface. |
| Polytechnique Montréal | N/A | Ely Cheikh Abass| [Robotique RL: QArm Reinforcement Learning (TD3, sim-to-real)](Polytechnique%20Montréal_ElyCheikhAbass_QArm_Reinforcement%20Learning/) | QArm | RL; Manipulation | TD3 reaching trained in QLabs (Virtual QArm) then validated on real QArm via QUARC; optional RealSense D415 + YOLO perception streamed to Simulink over UDP. |
| N/A | N/A | Archie James (@aj-floater), Thierry (@Thierryonre), Tara Mulhall (@tara257), UoM RoboSoc (@UoM-RoboSoc) | [QArm Hackathon Framework (PyBullet sim-to-real)](QArm_PyBullet%20Model) | QArm | Simulation; Manipulation | PyBullet `QArmSimEnv` with URDF/meshes; `SimQArm` wraps it behind a stable joint-angle API (`QArmBase`), and `api.make_qarm` is designed to switch between simulation and a stubbed `RealQArm` for later hardware parity. |
