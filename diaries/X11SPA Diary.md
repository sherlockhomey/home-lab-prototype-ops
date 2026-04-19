# Project Diary: X11SPA-T "Frankenstein" LLM Node
**Status:** Operational / Optimizing

---

## 1. Hardware Specifications
* **Motherboard:** Supermicro X11SPA-T.
* **System Memory:** 192GB DDR4 RAM.
* **GPU Cluster:** 12x AMD Radeon E8860 (GCN 1.0 architecture).
    * **Physical Layout:** 6x PCIe x16 slots; dual-chip custom boards.
    * **VRAM:** 2GB per chip (24GB total cluster VRAM).
* **Operating System:** Windows 11 LTSC.

---

## 2. Software Environment
* **Backend:** Native `llama.cpp` (Vulkan 1.2 build).
* **Front-end:** Open WebUI (Docker-based).
* **Test Model:** Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf.
    * **Model Size:** 4.36 GiB.
    * **Quantization:** Q4_K_M (Medium).

---

## 3. Benchmarking Results
The following metrics were recorded during the "Hello World" Python script generation test.

| Configuration | Prompt Speed (t/s) | Gen Speed (t/s) | Outcome |
| :--- | :--- | :--- | :--- |
| **CPU Only** | 13.22 | 7.81 | **Pass:** Coherent output. |
| **GPU (Flash Attention ON)** | 0.90 | 2.89 | **Fail:** Numerical corruption (`????`). |
| **GPU (FA OFF, Layer Split)** | 2.85 | 3.65 | **Pass:** Stable and coherent. |
| **GPU (FA OFF, Row Split)** | 2.85 | 3.81 | **Optimal:** Highest recorded GPU speed. |

---

## 4. Technical QA Observations

### **Critical Bug: Flash Attention Incompatibility**
* **Symptom:** Output consisted entirely of question marks (`????`).
* **Diagnosis:** GCN 1.0 legacy drivers do not support modern Flash Attention kernels.
* **Resolution:** Disabling Flash Attention via the `-fa 0` flag restored math accuracy.

### **Bottleneck: PCIe Synchronization**
* There is a **~78% drop** in prompt ingestion speed when moving from CPU to GPU (13.2 t/s vs 2.8 t/s).
* This is due to the overhead of synchronizing small data packets across 12 chips via the PCIe bus.

### **VRAM Fitting & Constraints**
* **OS Tax:** Windows display overhead consumes ~1120 MiB on the primary GPU (Vulkan11), limiting the "lowest common denominator" for the cluster.
* **Context Scaling:** To maintain a 100% GPU offload, the system automatically reduced the context window from 32,768 to 6,144 tokens.

---

## 5. Current Stable Launch Command
```powershell
.\build\bin\Release\llama-server.exe `
  -m "C:\ProgramData\LLModels\Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf" `
  --port 8080 `
  --host 0.0.0.0 `
  -ngl 999 `
  -sm row `
  -fa 0 `
  --cache-type-k f16 `
  --cache-type-v f16
```

---

## 6. Next Steps
* [ ] Connect Open WebUI (Docker) to the native Windows host server via `http://host.docker.internal:8080/v1`.
* [ ] Evaluate high-parameter models (30B+) to test 192GB RAM hybrid offloading.
* [ ] Explore `Q4_0` quantization to see if simpler math reduces PCIe overhead.
