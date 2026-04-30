# 📓 Diary: MSI Vector - AI Network Fabric Path

**Subject:** High-Performance Computing (HPC) & AI Network Automation
**Role:** The AI Network Engineer (The "Fabric" Manager)
**Primary Objective:** Transitioning from traditional "North-South" campus networking to high-bandwidth, self-healing "East-West" AI fabrics.

---

## 🧭 Phase 1: The "Crawl" (Environment & Connectivity)

### The Architectural Why: "Headless" Foundation
The foundational objective was building a stable Linux-based network emulation environment on Windows using WSL2 and Containerlab. In a production AI datacenter, physical access is rare; mastering the "headless" CLI environment is the first prerequisite for the AI Network Engineer role.

### The Mechanical How (Cheat Sheet)

| Task | Command / Action | Purpose |
| :--- | :--- | :--- |
| **Verify WSL** | `wsl --list --verbose` | Ensure WSL2 is active for Docker compatibility. |
| **Start Service** | `sudo service docker start` | Initialize the Docker daemon natively in Ubuntu. |
| **Deploy Lab** | `sudo clab deploy --topo clos.clab.yml` | Instantiate the virtual Leaf-Spine topology. |
| **Access Router** | `docker exec -it <node> vtysh` | Access the FRR routing engine CLI. |

---

## 🤖 Phase 2: The "Walk" (Underlay & BGP Unnumbered)

### The Architectural Why: The Clos Topology
Traditional 3-tier architectures using Spanning Tree Protocol (STP) are discarded in AI fabrics because they block redundant links to prevent loops. We implemented a **Leaf-Spine (Clos)** architecture where **ECMP (Equal Cost Multi-Pathing)** keeps every link active to maximize bandwidth.

By using **BGP Unnumbered**, we eliminated manual IP management for switch-to-switch links, allowing the fabric to self-discover neighbors via IPv6 Link-Local addresses.

### The Mechanical How (Cheat Sheet)

| Concept | Implementation | Role |
| :--- | :--- | :--- |
| **Loopbacks** | `11.11.11.11/32` | Acts as the stable "identity" anchor for the router. |
| **Unnumbered BGP**| `neighbor ethX interface remote-as external` | Peers via physical ports instead of IP addresses. |
| **Multipath** | `maximum-paths 2` | Enables load-balancing across both Spines simultaneously. |

### Mermaid Flow Charts 

## 1. Level 3: The "Mini-Fabric" (BGP Peering)
This was our first step into dynamic routing, showing a simple daisy-chain connection between two Leaf routers.

graph LR
   
    subgraph Clients
    PC1(PC1<br/>192.168.1.2)
    PC2(PC2<br/>192.168.2.2)
    end

    subgraph Fabric
    Leaf1(Leaf1<br/>ASN 65001)
    Leaf2(Leaf2<br/>ASN 65002)
    end

    PC1 ---|eth1| Leaf1
    Leaf1 ---|eth2: 10.0.0.1| Leaf2
    Leaf2 ---|eth1| PC2
    Leaf1 -.->|BGP| Leaf2

## 2. Level 4/5: The 2x2 Clos (Leaf-Spine) Physical Topology
This diagram reflects the "cross-hatch" pattern required for redundancy, where every Leaf connects to every Spine.

graph TD
   
    subgraph Spines
    Spine1[Spine1]
    Spine2[Spine2]
    end

    subgraph Leaves
    Leaf1[Leaf1]
    Leaf2[Leaf2]
    end

    subgraph Endpoints
    PC1(PC1)
    PC2(PC2)
    end

    %% Leaf 1 Connections
    Leaf1 ---|eth2| Spine1
    Leaf1 ---|eth3| Spine2
    
    %% Leaf 2 Connections
    Leaf2 ---|eth2| Spine1
    Leaf2 ---|eth3| Spine2

    %% PC Connections
    PC1 ---|eth1| Leaf1
    PC2 ---|eth1| Leaf2
---

## 🚀 Phase 3: The "Run" (EVPN-VXLAN Overlay)

### The Architectural Why: The "Magic Tunnel"
AI servers often require "Layer 2 Adjacency" (same subnet) even when separated by a routed fabric. We used **VXLAN** as a virtual teleporter to wrap Layer 2 frames inside Layer 3 packets. **EVPN** acts as the control plane "brain," sharing MAC addresses via BGP to prevent unnecessary broadcast traffic.

### The EVPN "Brain"
* **Type-2 Routes:** A shared "Phone Book" telling the fabric exactly which Leaf a specific MAC address lives behind.
* **Type-3 Routes:** A "Group Chat" that handles broadcast traffic (like ARP) so PC1 can find PC2 across the routers.

### Mermaid Flow Chart

## 3. Level 7: The Master Map (IP Fabric with EVPN-VXLAN)
This is the complete logical topology including the loopback IDs (VTEPs), ASNs, and the dual-layer (Underlay/Overlay) logic we implemented for the AI fabric.

graph TD
    
    subgraph "Spines (Route Reflectors)"
    S1["Spine1 (1.1.1.1)<br/>ASN 65021"]
    S2["Spine2 (2.2.2.2)<br/>ASN 65022"]
    end

    subgraph "Leaves (VTEPs)"
    L1["Leaf1 (11.11.11.11)<br/>ASN 65011"]
    L2["Leaf2 (22.22.22.22)<br/>ASN 65012"]
    end

    subgraph "Subnet: 192.168.1.0/24"
    P1(PC1)
    P2(PC2)
    end

    %% Underlay (Physical BGP)
    L1 === S1
    L1 === S2
    L2 === S1
    L2 === S2

    %% Overlay (VXLAN Tunnel)
    L1 -.->|VXLAN VNI 10| L2

    %% Client Links
    P1 --- L1
    P2 --- L2
---

## 🚨 Phase 4: The "War Room" (Failure Analysis)

### Failure 1: The PPA "NoneType" Error
* **Symptom:** `AttributeError: 'NoneType' object has no attribute 'people'` during Ansible installation via PPA.
* **Diagnosis:** A broken upstream dependency in the Ubuntu library used for PPA management within WSL.
* **The Cure:** Bypassed the PPA entirely and shifted to `pipx` for a clean, user-space Ansible installation.

### Failure 2: The "Split-Brain" Route
* **Symptom:** PC1 could not ping PC2 despite the BGP fabric being "UP."
* **Diagnosis:** The PC was trying to exit through the **Management Door** (eth0/Docker) instead of the **Data Door** (eth1/Leaf1).
* **The Cure:** Used `ip route del default` to remove the management gateway and forced traffic through the Leaf switch.

### Failure 3: The Ansible Collection "Phantom"
* **Symptom:** Ansible playbook failed with `couldn't resolve module/action 'frr_config'`.
* **Diagnosis:** Namespace mismatch; Ansible 2.16+ requires collections to be nested specifically inside an `ansible_collections` folder.
* **The Cure:** Purged the system installation, reinstalled via `pipx`, and forced collections into the standard `~/.ansible/collections` path.

---

## 🧠 Part 5: Key Jargon Glossary

* **Underlay:** The physical routing layer (BGP/IPv6) providing reachability between switches.
* **Overlay:** The virtual tunnel layer (VXLAN) where actual AI server traffic lives.
* **VTEP:** Virtual Tunnel End Point; the "entrance/exit" of the VXLAN tunnel.
* **ECMP:** Equal Cost Multi-Pathing; using multiple links for traffic simultaneously to maximize bandwidth.

## ENDPOINT ##

* Going to move this project to the Clevo machine to free up RAM space for LLM Inferencing and other things. Only 16GB DDR5 RAM currently. Need to upgrade
