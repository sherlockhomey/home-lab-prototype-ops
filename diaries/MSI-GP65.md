# MSI GP65 Leopard

## 🖥️ Machine Profile 
* **Role:** Primary Logic Hub / SDET Development Node.
* **Environment:** Windows 11 (Native Development).
* **Primary Duty:** Drafting architectural blueprints, framework scaffolding, and defining the "Contract" between the UI and Automation layers.

---

## 🏗️ Project: Agentic QA Sandbox (Initialization)
This machine serves as the "Master Blueprint" station. It is where we verify code integrity locally before shipping logic to the **Legion Pro 7 (Action Hub)** for heavy-duty pipeline execution.

### 🛠️ The Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Next.js 15 (App Router) | The target "Sandbox" application. |
| **Automation** | Playwright (TS) | The robot engine designed for POM-based testing. |
| **Logic Pattern** | Page Object Model (POM) | Decoupling element locators from test scripts. |
| **Sync Bridge** | TortoiseGit | GUI-based management for the GitHub "Source of Truth." |
| **Locator Strategy** | data-testid | Professional standard for stable, contract-based testing. |

---

## 📈 Milestone Log & Learning Points

### ✅ Phase 1: Infrastructure Scaffolding ("The Crawl")
* **Concurrent Scaffolding:** Initialized `next-js-app` and `playwright-framework` in isolated directories to prevent "Zombie Code" dependency bleeding.
* **Clean Slate Protocol:** Enforced strict `.gitignore` hygiene to ensure multi-gigabyte `node_modules` and `.next` caches are never pushed to the cloud.

### ✅ Phase 2: POM Integration ("The Walk")
* **Relative Pathing Logic:** Successfully moved from "Hardcoded GPS" (Absolute URLs) to "Environment Agnostic" testing. By setting a `baseURL` in the config, the code became portable between the MSI and the Legion.
* **Stable Locator Contract:** Implemented `data-testid`. Proved that the automation suite survives UI refactoring (e.g., changing button IDs) without failing, as long as the test ID remains constant.

### ✅ Phase 3: Repository Isolation ("The Polyrepo Pivot")
* **Surgical Extraction:** Organized the MSI workspace into a Polyrepo structure. Created the `agentic-qa-sandbox` folder to house the specific project Monorepo sit side-by-side with the pre-existing Ops and Skeleton repos.
* **The GitHub Bridge:** Successfully initialized the Git state via TortoiseGit and pushed the baseline to the "Action Hub" (GitHub) for Jenkins consumption.

---

## 🔌 Connectivity Map
`[MSI GP65 (Logic Hub)] -> [GitHub (The Source)] -> [Legion Pro 7 (Action Hub / Jenkins)]`

---

## ⚠️ Troubleshooting "Cheat Sheet"
* **Working Directory Errors:** Always ensure the terminal is at the "Root" of the specific project (where `package.json` lives) before running `npm` commands.
* **TortoiseGit Overlay Icons:** * **Green Check:** Logic is in sync with the cloud.
    * **Red Exclamation:** Local logic has drifted (Commit required).