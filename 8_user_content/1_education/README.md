<div align="center" style="margin-bottom:24px;">
  <div style="width:100%; max-width:1300px; aspect-ratio: 2 / 1; overflow:hidden; border-radius:9px;">
    <img img src="../images/header_user_generated_content_education.png"
         alt="Header"
         style="width:100%; height:100%; object-fit:cover; display:block;" >
  </div>
</div>


## Education

![Category](https://img.shields.io/badge/category-education-2ea44f?style=flat-square)
![Platforms](https://img.shields.io/badge/platforms-QCar%20%7C%20QDrone%20%7C%20Qube%20%7C%20Aero%20%7C%20QLabs-8250df?style=flat-square)
![Areas](https://img.shields.io/badge/areas-Control%20%7C%20Modeling%20%7C%20SysID%20%7C%20SLAM%20%7C%20RL%20%7C%20MPC-ffb000?style=flat-square)

Educators around the world extend Quanser academic resources with course projects and lab-style activities, from ready-to-run labs to adaptable student projects. In this section you will find examples such as SLAM on QCar, nonlinear modeling and controller design on Aero, and RL/MPC benchmarks on Qube.

> **Note on credit:** All credit remains with the original authors. Each entry links back to the source material.

---

### Education index

| Institution | Author(s) | Title | Platform | Domain | Format | What you get |
|---|---|---|---|---|---|---|
| Miami University | Daniel Wood | [QCar SLAM (FastSLAM)](Miami%20university_QCar_PythonSLAM_FastSLAM) | QCar 1 | SLAM | Python | Grid-based FastSLAM with particle filter + occupancy-grid mapping using wheel encoders and LiDAR; includes a practical run workflow. |
| Politecnico di Milano | Francesco Berruti; Alessandro Donadi; Fausto Allegrini; Ahmad Labib; Lorenzo Marzi | [Quanser Aero Control Project (nonlinear modeling + control)](Politecnico%20di%20milano_ControlLab_QuanserAero_NonlinearModelParamID) | Quanser Aero | Modeling; SysID; Control | MATLAB/Simulink | Full pipeline: derive nonlinear dynamics (Lagrangian) → identify parameters from experimental data → linearize → design/compare controllers (PD/PID, LQ/LQ-TV, LMI, nonlinear MPC). |
| Shanghai Jiao Tong University | gongchenooo (repo handle) | [RL and Learned-Model MPC Benchmarks (simulation)](Shanghai%20Jiao%20Tong%20university_Qube_BallBalancer_Cartpole_TRPO_LearnedDynamicsMPC) | Qube (sim); Ball Balancer (sim); Cartpole (sim) | RL; MPC | Python + report | TRPO (model-free) vs learned-dynamics planning (model-based RL style MPC), plus optimizer comparisons; includes a PDF report for the experiments. |
| Thunking Oasis | AlbaraaAlkilani (repo handle) | [Dual-Agent DRL for Modular Qube-Servo 2 Control](Thunking%20Oasis_AlbaraaAlkilani_QubeServo2_SimulatedDualAgentModularDRL) | Qube-Servo 2 | RL | MATLAB/Simulink | Simulink `.slx` models + saved agents and demos for staged/modular RL control (e.g., swing-up and balance as separate agents). |
| Universidad de Ingeniería y Tecnología | GabrielEGC (repo handle) | [rl_qube: RL from Scratch](Ingeniería%20y%20Tecnología%20University_QubeServo_RLFromScratch) | Qube-Servo 2 | RL | MATLAB/Simulink; C++ | From-scratch RL components (no libraries) with Simulink scaffolding; includes a CPU-trained DQN implementation in C++ for comparison/extension. |
Ostfalia University of Applied Sciences | Dennis Marvin Lank| [QArm Web Dashboard for Control and AI Perception](Ostfalia%20Univ%20of%20Applied%20Sciences_QArm_Web_Dashboard_for_Control_and_AI_Perception)| QArm| HMI; Vision; AI-assisted manipulation| Python (Dash); QUARC; MySQL| Local web dashboard for QArm manual control (joints, Cartesian, LEDs), live RGB/depth view, YOLOv11 object detection with scan and pick/place flow, plus STT/TTS voice commands and YOLO model management. |
Queen's University | Noah Waisbrod | [neural-networks-for-real-time-CV-control-of-a-Quanser-QArm](Queen's%20university_NoahWaisbrod_QArm_Real-time_Gestur_and_&Object_Detection) | QArm| Vision; HRI; AI-assisted manipulation| Python| Student lab project: real-time hand-gesture gripper control plus live YOLOv8n object-detection overlay on the QArm RealSense RGB stream (OpenCV loop).|
| N/A | Wang Ziyi (@Azi2333) | [Line Following on QBot Platform (Classical + CNN)](QBot%20Platform_lineFollowing_Wang%20Ziyi_Classical-AI) | QBot Platform (QLabs) | Computer Vision; Control; Applied AI | Python | Two QLabs implementations for line following: a classical thresholding + centroid + kinematic control baseline, and a CNN classifier pipeline with training, real-time inference, and evaluation for comparison. |