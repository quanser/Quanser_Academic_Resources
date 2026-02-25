# Semantic Edge–Cloud Traffic Surveillance with ViT + LLMs (QLabs Dataset)

![Urban Mobility Research Dataset (Video Records, QLabs)](https://ieee-dataport.org/sites/default/files/styles/home/public/Screenshot%202025-10-30%20112931.png.webp?itok=wjPAS5bt)
<!-- Image source: IEEE DataPort dataset page (“Urban Mobility Research Dataset (Video Records) Generated with Quanser Interactive Lab”). -->

## Overview

This work studies how to use **cloud-hosted multimodal LLMs** for **real-time urban traffic surveillance** when edge cameras produce high-resolution video but the wireless link has **bandwidth/latency limits**.

The key idea is **semantic communication**: instead of streaming full frames, the edge extracts **vehicle-centric regions of interest (RoIs)**, converts them into compact **ViT embeddings**, transmits those embeddings, then reconstructs a small image crop in the cloud for **LLM-based traffic descriptions and Q&A** (reported using LLaVA-style models).

---

## How the Quanser Community Can Use This

- **Fast start for edge–cloud AI:** use the dataset as a drop-in benchmark for “send less than pixels” pipelines (crop, compress, embed, transmit, reconstruct).
- **Test your own semantic payloads:** compare raw crops vs **ViT embeddings** vs alternative compact representations (different ViTs, autoencoders, learned codecs).
- **Study link realism:** evaluate how quantization, modulation/channel noise, latency budgets, or packet loss change downstream task quality (caption accuracy, incident detection).
- **Build better traffic assistants:** expand captions into operator-style Q&A pairs (risk, right-of-way, congestion level), or move from single-frame to short temporal windows.
- **Extend the dataset in QLabs:** generate more scenarios (lighting/weather, occlusion, dense pedestrians, near-misses), add annotations (speed/heading/TTC), and publish a larger benchmark suite.

---

## Experimental Setup

- **Environment:** Quanser Interactive Labs (QLabs) urban traffic scene with scripted scenarios
- **Capture:** fixed surveillance cameras producing **2048×2048 RGB** frames with timestamps (video records)
- **Edge perception (reported):** vehicle detection/segmentation → square RoI cropping (scaled context) → resize to **224×224**


---

## Stack / Tags

**Tags:** `QLabs` `Dataset` `Edge–cloud AI` `Semantic communication` `Multimodal LLM` `Traffic surveillance` `Wireless/mobile networks`

---

## Links

- **Dataset (IEEE DataPort):**  
  https://ieee-dataport.org/documents/urban-mobility-research-dataset-video-records-generated-quanser-interactive-lab

- **Paper (arXiv):**  
  https://arxiv.org/abs/2509.21259v1

---

## Lab / Affiliation

University of Ottawa — Smart Connected Vehicles Innovation Centre (SCVIC)

---

## Authors

Murat Arda Onsu · Poonam Lohan · Burak Kantarci · Aisha Syed · Matthew Andrews · Sean Kennedy
