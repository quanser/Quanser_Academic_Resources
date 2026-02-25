# Leveraging Multimodal-LLMs + Instance Segmentation for Traffic Monitoring (QLabs Dataset)

![Urban Mobility Research Dataset (QLabs)](https://ieee-dataport.org/sites/default/files/styles/home/public/img_291_0.jpg.webp?itok=NZnT0jeL)
<!-- Image source: IEEE DataPort dataset page (“Urban Mobility Research Dataset (Generated with the Quanser Interactive Lab)”). -->

## Overview

This work targets a practical **traffic-monitoring assistant**: given **multi-camera urban scenes**, answer operator-style questions (vehicle locations, movement/steering direction, congestion/collision awareness) clearly and consistently.

The key contribution for the community is the **dataset + reproducible QLabs setup**: scenes are generated safely in simulation (including rare events like collisions) and labeled automatically using simulator ground truth, reducing the need for manual annotation.

**Catch:** Instead of feeding raw images directly to a multimodal LLM, they first apply **instance segmentation (YOLOv11s)** to emphasize dynamic objects (vehicles, pedestrians) and fine-tune **LLaVA 1.5** with **LoRA**. They also train the model to output **generic location aliases** and map them to real road names via an external lookup table, improving portability across camera deployments.

---

## How the Quanser Community Can Use This

- **Fast start for teaching/research:** use the dataset to fine-tune or evaluate a traffic VLM on realistic, repeatable scenarios (including congestion and collision cases).
- **Benchmark modular pipelines:** compare *raw-image VLM* vs *segmentation-first VLM* on the same prompts and accuracy metrics (location, direction, incident awareness).
- **Reuse the “alias + lookup table” pattern:** keep the model camera-agnostic (section aliases), then remap aliases to your own road names per camera without retraining from scratch.
- **Scale it up in QLabs:** script more scenarios (weather/lighting, occlusion, dense pedestrians, near-misses) and regenerate labels automatically using QLabs ground-truth coordinates.

---

## Experimental Setup

- **Environment:** Quanser Interactive Labs (QLabs) urban scene with controllable roads, vehicles, pedestrians, signs, and lights.
- **Cameras:** 4 non-overlapping cameras placed around the environment (combined coverage of the full scene).
- **Capture:** data collected every **5 ms**, at **1024×1024** resolution.
- **Scenarios:** **30** driving scenarios (intersections, roundabouts, 4-way junctions, one-way roads, etc.), including **7** scenarios with collision events.
- **Dataset:** **800** images with automatically generated textual descriptions (captions).
- **Perception assist:** **YOLOv11s** instance segmentation for vehicles and pedestrians.

---

## Stack / Tags

**Tags:** `QLabs` `Traffic monitoring` `Multimodal LLM` `LLaVA-1.5` `LoRA` `YOLOv11` `Instance segmentation` `Synthetic dataset`

---

## Links

- **Dataset (IEEE DataPort):**  
  https://ieee-dataport.org/documents/urban-mobility-research-dataset-generated-quanser-interactive-lab

- **Paper (arXiv):**  
  https://arxiv.org/abs/2502.11304

---

## Authors

Murat Arda Onsu · Poonam Lohan · Burak Kantarci · Aisha Syed · Matthew Andrews · Sean Kennedy
