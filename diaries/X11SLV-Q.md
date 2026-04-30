# Supermicro X11SLV-Q (CRS)

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
| **RAM** | 16GB DDR3 |
| **GPU** | Discrete 4GB VRAM (Media Offload) |
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
```
📈 Current Workflows & Study Guides
GitHub Machine Diary: Automated tracking of lab-wide hardware changes.

Agentic Logic Gates: Routing logic requests between the MSI Vector and Legion Pro 7.

4K Media Playback: Verified smooth 4K decoding using the discrete 4GB GPU while n8n manages background triggers.

## 🎓 Study Guide: AI Orchestration & Infrastructure

### 1. Persistence vs. Ephemerality (The Docker Lesson)
**Concept:** Containers are "disposable," but data is "permanent."
- **Importance:** If you store your n8n workflows inside the container, they vanish when the container stops.
- **Implementation:** We used **Named Volumes** (`n8n_data`). Even when we deleted the n8n container and image, the "Soul" (database.sqlite) survived on the hidden virtual disk.
- **Actionable:** Always use `external: true` in your compose file once a volume is created to prevent accidental resets.

### 2. State Awareness (The "Gatekeeper" Logic)
**Concept:** The "Brain" should only think when there is something new to think about.
- **Importance:** Running an LLM (MSI Vector) takes power and heat. Polling GitHub every minute without a filter wastes resources.
- **Implementation:** We used `$getWorkflowStaticData` in an n8n JavaScript node. 
- **The Logic:** We save the "SHA" (digital fingerprint) of the diary file. If the SHA hasn't changed since the last run, the workflow stops immediately, sparing the MSI Vector's GPU.



### 3. Data Engineering for LLMs (Slicing & Context)
**Concept:** Large Language Models (LLMs) have a "Context Window" (Maximum memory).
- **Importance:** Sending a 15-page markdown diary to an AI for a 1-sentence command causes "Context Dilution." The AI gets lost in the noise.
- **Implementation:** We used `.slice(-1500)` to only send the most recent 1,500 characters of the diary.
- **The "Wizard" Note:** This ensures the AI sees your `[SYSTEM_COMMAND]` at the bottom of the file with 100% clarity.



### 4. Middleware Sanitization (`JSON.stringify`)
**Concept:** APIs speak JSON; humans speak Markdown.
- **Importance:** Markdown uses quotes and newlines that "break" JSON envelopes.
- **Implementation:** Wrapping the diary content in `JSON.stringify()`.
- **The Result:** It turns messy human text into a "Safe String" that can travel across the network to the MSI Vector without crashing the API call.

### 5. The Distributed Cluster Pattern
**Concept:** Decoupling the Executive, the Brain, and the Muscle.
- **The Executive (X11):** High availability, low power, 24/7 monitoring.
- **The Brain (MSI Vector):** High compute, high power, on-demand reasoning.
- **The Muscle (Legion):** Dedicated execution, CI/CD, physical browser testing.
- **Importance:** This mimics an Enterprise microservices architecture. If the MSI Vector goes offline, the X11 still monitors the lab. If the Legion is busy, the X11 queues the tasks.

📝 Future Milestones
[ ] Integration: Deploying telemetry monitoring for the entire home lab.

[ ] SLM Logic Scout: Implementing a localized Phi-3-Mini model (CPU-based) for basic log classification.

[ ] Ansible Handshake: Integrating the X11 as the primary control node for fleet-wide software updates.
