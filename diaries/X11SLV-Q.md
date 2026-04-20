# Machine Diary: Supermicro X11SLV-Q (CRS)

## 🖥️ System Profile
- **Hostname:** CRS-X11
- **Role:** Primary Lab Orchestrator (n8n Brain) & 4K Media Node
- **IP Address:** `192.168.1.6`
- **Operating System:** Windows 11 Pro / Docker Desktop (WSL2 Backend)

## 🛠️ Hardware Specifications
| Component | Detail |
| :--- | :--- |
| **Motherboard** | Supermicro X11SLV-Q (Mini-ITX) |
| **CPU** | Intel® Core™ i7-4700 series (Haswell Refresh) |
| **RAM** | 16GB DDR3L |
| **GPU** | Discrete 2GB VRAM (Media Offload) |
| **Networking** | Dual Intel® GbE LAN |

---

## 🧠 Lab Architecture Evolution
Originally considered for a "Logic Scout" agentic role, the machine has been promoted to **Primary Orchestrator**. 

### The "Brain-Shift" Migration
On April 20, 2024, the n8n orchestration hub was migrated from the **Clevo P65** (Worker Node) to this **X11SLV-Q** (Management Node). 

**Technical Challenges Overcome:**
1. **WSL Pathing:** Navigating the internal Docker Desktop volume path (`\\wsl.localhost\docker-desktop...`).
2. **Volume Persistence:** Utilized a "Named Volume" strategy (`n8n_data`) to decouple the application logic from the filesystem.
3. **The "Alpine Bridge" Transfer:** Used a temporary Linux container to bridge the Windows `C:\` drive and the internal Docker volumes via `tar` compression to preserve SQLite database permissions.

---

## 🚀 Deployment Configuration
The machine runs n8n in a persistent Docker container with a "Restart Always" policy to ensure lab-wide automation is never offline.

### Docker Compose Snippet
```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n-brain
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=192.168.1.6
      - WEBHOOK_URL=[http://192.168.1.6:5678/](http://192.168.1.6:5678/)
      - TZ=America/Los_Angeles
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
    external: true
📈 Current Workflows & Study Guides
GitHub Machine Diary: Automated tracking of lab-wide hardware changes.

Agentic Logic Gates: Routing logic requests between the MSI Vector and Legion Pro 7.

4K Media Playback: Verified smooth 4K decoding using the discrete 2GB GPU while n8n manages background triggers.

📝 Future Milestones
[ ] Technical Wizard Integration: Deploying telemetry monitoring for the entire home lab.

[ ] SLM Logic Scout: Implementing a localized Phi-3-Mini model (CPU-based) for basic log classification.

[ ] Ansible Handshake: Integrating the X11 as the primary control node for fleet-wide software updates.
