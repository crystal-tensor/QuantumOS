# Project Task Board

## 🚀 Milestones & Roadmap

### Phase 1: Core Architecture (Completed)
- [x] **Project Initialization**: Setup git repository and directory structure.
- [x] **Architecture Design**: Define 4-layer architecture (App, Kernel, HAL, Hardware).
- [x] **Backend Implementation**:
    - [x] Develop `kernel_rust` with MLFQ scheduler and qubit resource management.
    - [x] Create FastAPI backend (`dashboard/app.py`) for handling requests and process management.
- [x] **Frontend Dashboard**:
    - [x] Design `index.html` with real-time log monitoring.
    - [x] Implement SVG-based architecture visualization with data flow animations.
    - [x] Add dual-path visualization (Real QPU vs. Simulator).

### Phase 2: Quantum Algorithms & Workflow (Completed)
- [x] **VQE Implementation**:
    - [x] Create `generate_vqe_workflow.py` for 4-qubit H2 molecule simulation.
    - [x] Implement Hardware Efficient Ansatz (HEA) visualization.
    - [x] Generate pulse sequences with CR and Echo pulses.
    - [x] Map logical circuit to physical 2x3 grid topology.
- [x] **Heterogeneous Hardware Support**:
    - [x] Create `generate_alternatives.py` for Neutral Atom and Ion Trap workflows.
    - [x] Visualize Rydberg Blockade and Raman Laser operations.
- [x] **Error Correction**:
    - [x] Create `generate_surface_code_gif.py` for Surface Code cycle animation.

### Phase 3: Documentation & Intellectual Property (In Progress)
- [x] **Project Documentation**:
    - [x] Create detailed `README.md` (Chinese).
    - [x] Create detailed `README_EN.md` (English).
- [x] **Patent Disclosures**:
    - [x] Draft Patent 1: Multi-Layer Architecture & QOS-DP Protocol.
    - [x] Draft Patent 2: QISA to QIR Compilation Method.
- [ ] **Business Plan**:
    - [x] Draft initial Business Plan (market analysis, financial projections).
    - [ ] Refine financial model with more granular data (Future).

### Phase 4: Integration & Testing (Ongoing)
- [x] **System Integration**:
    - [x] Connect Dashboard to Rust Kernel via API.
    - [x] Enable "Start Kernel" and "Run SDK" functionalities.
- [ ] **Unit Testing**:
    - [ ] Add unit tests for Rust Scheduler.
    - [ ] Add integration tests for Python SDK.
- [ ] **CI/CD**:
    - [ ] Setup GitHub Actions for automated build and test.

## 📝 Current To-Do List

### High Priority
- [ ] **Refine API Documentation**: Auto-generate Swagger/OpenAPI docs for FastAPI endpoints.
- [ ] **Add User Auth**: Implement simple JWT authentication for the Dashboard.
- [ ] **Optimize Visualization**: Improve performance of SVG animations on low-end devices.

### Medium Priority
- [ ] **Expand SDK**: Add support for QAOA and Grover's algorithm examples.
- [ ] **Docker Support**: Create `Dockerfile` and `docker-compose.yml` for easy deployment.
- [ ] **Cloud Connector**: Implement a mock interface for connecting to AWS Braket or IBM Quantum.

### Low Priority / Nice to Have
- [ ] **Dark Mode**: Add dark mode toggle for the Dashboard.
- [ ] **Multi-language Support**: Translate Dashboard UI to Chinese/English.

## 🐛 Known Issues / Bugs
- *None at the moment.*

## 📅 Changelog

### v0.1.0 - Initial Release
- Released core kernel with MLFQ scheduler.
- Launched web dashboard with real-time visualization.
- Added support for VQE workflow generation.
- Completed heterogeneous hardware mapping (Superconducting, Ion Trap, Neutral Atom).
