# 📔 Diary: Lenovo Legion 7i Pro

## 🖥️ Machine Profile
* **Role:** Dedicated CI/CD Development & QA Automation Node.
* **Environment:** Windows 11 Home/Pro (Native).
* **Primary Duty:** Hosting the "Skeleton" Infrastructure for enterprise-grade Playwright testing and Jenkins orchestration.

---

## 🏗️ Project: Playwright-Skeleton CI/CD
This project serves as the foundational "Rack" for transitioning from manual A/V testing to automated, agentic-ready QA workflows.

### 🛠️ The Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestrator** | Jenkins (LTS) | The "Brain" – executes the Jenkinsfile pipeline. |
| **Automation** | Playwright (TS) | The "Muscle" – handles UI and API interactions. |
| **Version Control** | Git / GitHub | The "Memory" – secure, private code storage. |
| **GUI Git Client** | TortoiseGit | The "Dashboard" – visual management of commits/pushes. |
| **The Tunnel** | ngrok | The "Bridge" – secure public entry for GitHub webhooks. |
| **Runtime** | Node.js (v24) | The "Engine" – environment for running Playwright/npm. |

---

## 📈 Milestone Log & Learning Points

### ✅ Phase 1: The Local Foundation ("The Walk")
* **Jenkins as a Service:** Successfully installed Jenkins on Windows 11. Overcame initial security hurdles by modifying `jenkins.xml` to allow **Local Checkout**.
* **Pipeline as Code:** Transitioned from manual Jenkins jobs to a `Jenkinsfile`.
* **The CSP Wall:** Identified why HTML reports look "broken" in Jenkins. Blanked the CSP property in `jenkins.xml` for full CSS/JS rendering.

### ✅ Phase 2: External Connectivity ("The Run")
* **The ngrok Handshake:** Mapped `localhost:8080` to a static public domain. Bypassed router firewall limitations safely.
* **Webhook Synchronization:** Wired GitHub to "poke" Jenkins on every push.
* **The "Exit 0" Trap:** Discovered that `|| exit 0` masks failures. Removed it to allow Jenkins to record "Red Builds" for honest QA results.

### 🕒 Phase 3: The Fuller Environment (In Progress)
* **The "Rack" Analogy:** Evolving from a single "Bare" item to a multi-stage pipeline.
* **API Integration:** Adding `api.spec.ts` to test the logic layer without browser overhead.
* **n8n Synergy:** Preparing for remote triggers via API Tokens.

---

## 🔌 Connectivity Map
`[Local Code] -> [TortoiseGit Commit] -> [GitHub Push] -> [Webhook Signal] -> [ngrok Tunnel] -> [Jenkins Execution] -> [HTML Report]`

---

## ⚠️ Troubleshooting "Cheat Sheet"
* **Locked out of Jenkins?** Edit `config.xml` and set `<useSecurity>` to `false`, restart service.
* **Webhook not triggering?** Verify the Repository URL in Jenkins matches the GitHub HTTPS URL.
* **Tests passing but Build Red?** Check for `exit 1` codes in the console log.
