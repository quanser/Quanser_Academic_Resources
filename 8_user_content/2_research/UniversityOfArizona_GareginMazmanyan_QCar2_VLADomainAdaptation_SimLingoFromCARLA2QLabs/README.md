# Adapting VLA Driving Models to QLabs: A SimLingo Case Study on the QCar2

## Overview
This MS thesis takes SimLingo, a state-of-the-art vision-language-action (VLA) driving model trained in the CARLA simulator, and adapts it to drive the QCar2 in Quanser QLabs. A VLA model looks at a camera image and a route goal and predicts where the car should go. The problem is that a model trained on CARLA's graphics does not transfer to QLabs' different graphics: dropped in directly, it covered only 4.7% of the route.

The thesis treats this as a distribution-alignment problem rather than a modeling one. It freezes the large pretrained model and uses LoRA to adapt a small fraction of it to the new visuals, then matches the inference-time signals (coordinate frames, control rate, steering sign, speed estimation) to what the model saw during training. After adaptation the model follows the route as precisely as the human expert (0.085m vs 0.087m displacement error) and reacts to obstacles from the camera alone, though a classical LiDAR baseline still stops more reliably. The result is a reproducible pipeline (expert data collection, LoRA fine-tuning, real-time inference, and evaluation) that opens a path for bringing CARLA-trained driving models onto the QCar2 platform.

---

## How the Quanser Community Can Use This
- A documented path to bring CARLA-trained driving models onto the QCar2, with the physical 1/10 QCar2 as the natural next step.
- A reusable method: collect target-platform data, match the original model's interface, fine-tune efficiently with LoRA, align the control loop, and evaluate against a strong baseline.
- A worked example of parameter-efficient fine-tuning (LoRA) for moving a large model into a new visual domain with only a few thousand frames, instead of full retraining.
- A learned-versus-classical comparison on the same task: a vision-only VLA policy against a LiDAR-based adaptive cruise control baseline, giving real numbers for that tradeoff.
- Use it in autonomous driving, imitation learning, VLA, control, and simulation-transfer courses or thesis projects.
- Extend it to new routes, unseen obstacles, temporal camera inputs, multiple sensors, or physical QCar2 validation. The workflow is validated with one model on one main QLabs route in simulation, so it is a reusable method rather than a universal transfer tool yet.

---

## Experimental Setup
- **Platform:** Quanser QLabs Virtual QCar2
- **Model:** SimLingo, a VLA policy built on InternVL2-1B (frozen InternViT-300M vision encoder plus a Qwen2-0.5B language model)
- **Software and language:** Python, with the Quanser SDK
- **APIs / Libraries:** PyTorch, PyTorch Lightning, DeepSpeed, LoRA/PEFT, Hydra, OpenCV, Weights & Biases
- **Note:** evaluated on one roundabout route with five static-obstacle placements; not yet tested on the physical QCar2 (flagged as future work)

---

## Stack / Tags
`Python`, `PyTorch`, `VLA`, `Vision-Language-Action`, `LoRA`, `PEFT`, `SimLingo`, `Imitation Learning`, `Sim-to-Sim Transfer`, `PID Control`, `QCar2`, `QLabs`

---

## Links
- **GitHub Repository:**  
https://github.com/tothelast/Qcar2SimDev

- **Project Page:**  
https://gareginmazmanyan.com/projects/vla.html

- **Thesis / Report:** https://www.proquest.com/openview/a7b53e648a8e9a87ec222c6e4c9862be/1?pq-origsite=gscholar&cbl=18750&diss=y

---

## Author
Garegin Mazmanyan  
MS Thesis, Computer Science, University of Arizona