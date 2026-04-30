# Clevo P65: Technical Diary & Study Guide

## 🖥️ System Profile
- **Hostname:** CLEVO-P65
- **Role:** HPC / AI Study Node & Containerlab Testing Hub
- **Former Role:** Legacy Lab Orchestrator (Migration to X11 CRS complete)
- **Operating System:** Windows 11 / Docker Desktop (WSL2)

## 🛠️ Hardware Specifications
| Component | Detail |
| :--- | :--- |
| **System** | Clevo P65 Series Laptop |
| **GPU** | NVIDIA GeForce GTX 980M 8GB |
| **RAM** | 32GB DDR3 |
| **Network** | Ethernet via Sonic Fiber LAN |


## 🎓 Study Guide: The Orchestration Era
During Phase 1, the Clevo served as the **"Executive"** of the lab.

### 🧠 Core Concepts Learned
1. **The Distributed Relay Race:** Learned to coordinate tasks across three physical machines (Clevo → MSI Vector → Legion).
2. **Infrastructure as Code (IaC):** Used `docker-compose.yaml` to define the entire n8n environment, ensuring repeatability.
3. **The Executive/Worker Pattern:** Decoupling the "Thinking" (AI reasoning) from the "Doing" (Jenkins execution).
4. **State Persistence:** Understanding that a container's "memory" (workflows/credentials) must live in a persistent **Volume**, not in the container itself.

---

## 📝 Cheat Sheet: n8n & Docker Operations
### Essential Commands
| Command | Purpose |
| :--- | :--- |
| `docker-compose up -d` | Launch n8n in the background (detached mode). |
| `docker volume ls` | Audit surviving data disks (The "Soul" of the lab). |
| `docker ps` | Verify the "Brain" container is running and healthy. |
| `docker logs n8n-brain` | Read the internal logs for troubleshooting. |

### The "Sacred" Docker Compose Snippet
```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n-brain
    restart: always
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
    external: true
```

## 🛠️ Incident Report: The Volume Resurrection
**Scenario:** Accidentally deleted the n8n container and image during an update.
**The "Wizard" Lesson:** - Containers are ephemeral (they die easily). 
- Images are the blueprints.
- **Volumes are the Vault.** **Recovery Protocol:** 1. Run `docker volume ls` to confirm `n8n_data` still exists.
2. Run `docker-compose up -d` to rebuild the container and "plug it back in" to the surviving vault.
3. Your workflows and credentials will be intact because they were stored safely on the virtual disk.

---

## 🔄 The Great Reorganization
As of April 2026, the Orchestration Brain has migrated to the **Supermicro X11 CRS**.

### New Mission for CLEVO-P65:
- **HPC Node:** Utilizing the RTX 980M for intensive local inference prototyping.
- **Network Lab:** Hosting **Containerlab** to simulate complex leaf-spine network topologies.
- **Logic Scout:** A sandbox for developing new Playwright and Ansible scripts before they are pushed to the X11 production instance.

**Last Technical Audit:** 2026-04-22
**Status:** Online - Worker Node
