# 光谱 QuantumOS (QOS) 多智能体协同开发计划 v1.0

**项目愿景:** 构建跨硬件、时间感知、内置纠错的统一量子操作系统。
**开发模式:** 人机协同 (Human-in-the-Loop) + 多智能体并发开发 (Multi-Agent Collaboration)
**人类统帅 (总指挥):** 负责顶层架构、API 边界仲裁、跨模块集成测试与物理逻辑验证。

---

## 一、 Agent 团队组建与角色定义

为了实现分层解耦的架构，我们需要实例化 4 个具有不同专业技能和 System Prompt 的核心 Agent。



| Agent 代号 | 核心角色 & 技术栈 | 职责边界 (System Prompt 核心指令) | 交付物 |
| :--- | :--- | :--- | :--- |
| **Agent-Alpha (内核组)** | 顶级 Rust 系统程序员 | 专注内存安全与极速响应。你负责 QOS 内核层，绝对禁止使用会阻塞线程的库。你需要实现基于物理寿命（相干时间）的非抢占式优先级调度器。 | `kernel/` 目录下的 Rust 源码，调度算法。 |
| **Agent-Beta (编译组)** | C++/LLVM 编译器专家 | 专注指令集转换。你需要将 SQISA (光谱量子指令集) 映射为 QIR (量子中间表示) 标准。精通 LLVM IR 与 AST 解析。 | `compiler/` 目录下的 C++ 代码，LLVM Pass。 |
| **Agent-Gamma (物理组)** | 量子物理学家 & QEC 专家 | 精通超导/离子阱底层控制与纠错。你需要用 Python/C++ 编写基于表面码的纠错逻辑 (QEC)，以及 Q-Sim 数字孪生模拟器的物理噪声注入模块。 | `q_sim/` 与 `qec_engine/` 目录的代码与数学模型。 |
| **Agent-Delta (生态组)** | Python 高级架构师 | 专注开发者体验。你需要编写面向最终用户的应用层 SDK，实现 `@quantum_task` 等优雅的 API 装饰器，并处理 Python 与 Rust 内核的跨语言通信 (PyO3)。 | `sdk/` 目录下的 Python 源码，开发者文档。 |

---

## 二、 分阶段协同开发路线图 (Roadmap)

### 阶段 1: 基础设施与数字孪生 (Month 1)
**目标:** 搭建系统骨架，并在没有真实硬件的情况下，跑通带有物理噪声的模拟器。

* **Task 1.1: 确立 SQISA 指令集标准**
    * **执行者:** 人类统帅 + Agent-Gamma (物理组)
    * **动作:** 共同敲定最初的 10 条核心汇编指令（如 QALLOC, U3, WAIT）。
* **Task 1.2: 研发 Q-Sim 模拟器**
    * **执行者:** Agent-Gamma (物理组)
    * **动作:** 用 Python 编写模拟器，注入 $T_1$、$T_2$ 寿命参数和门保真度。
    * **协同要求:** 向 Agent-Alpha 提供模拟器的输入输出 API 格式。
* **Task 1.3: 构建 Rust 内核调度器雏形**
    * **执行者:** Agent-Alpha (内核组)
    * **动作:** 实现 `SpectrumQScheduler`，使用二叉堆管理任务队列，能根据 Q-Sim 提供的寿命阈值拒绝或执行任务。

### 阶段 2: 编译器桥接与 SDK 体验 (Month 2)
**目标:** 打通从 Python 应用层到中间表示 (QIR) 的全链路。

* **Task 2.1: Python SDK 骨架开发**
    * **执行者:** Agent-Delta (生态组)
    * **动作:** 编写 `spectrum_os` 库，实现 `@quantum_task` 装饰器，将高级代码打包成 JSON/RPC 格式发给内核。
* **Task 2.2: Python-Rust IPC 通信**
    * **执行者:** Agent-Delta (生态组) & Agent-Alpha (内核组) 协同
    * **动作:** 使用 `gRPC` 或 `PyO3` 实现 SDK 进程与 Rust 内核进程的高效通信。**人类统帅需在此介入，审查接口契约 (Interface Contract)。**
* **Task 2.3: SQISA 到 QIR 的编译映射**
    * **执行者:** Agent-Beta (编译组)
    * **动作:** 接收内核下发的 SQISA 任务流，生成符合微软标准的 C++ LLVM IR 文本。

### 阶段 3: 量子纠错 (QEC) 与硬件抽象层 (Q-HAL) (Month 3)
**目标:** 加入纠错保护膜，并编写第一个真实硬件的适配驱动（超导微波）。

* **Task 3.1: 表面码解码器实现**
    * **执行者:** Agent-Gamma (物理组)
    * **动作:** 编写 MWPM (最小权完美匹配) 算法，集成到内核的执行流中。
* **Task 3.2: 研发超导驱动 (Q-HAL 伪代码)**
    * **执行者:** Agent-Beta (编译组) + Agent-Gamma (物理组) 联合执行
    * **动作:** 将 QIR 函数 (`__quantum__qis__u3__body`) 解析为带包络的微波高斯脉冲序列数组。

---

## 三、 你的统帅工作流 (Daily Operations)

为了防止 AI Agents 产生幻觉或系统架构偏离，你需要执行以下每日工作流：

1.  **分发 Prompt (Morning):**
    * 每天启动时，明确每个 Agent 的当日任务。
    * *示例 (给 Agent-Alpha):* "今天你需要完善 `scheduler.rs`。昨天 Agent-Gamma 已经更新了 `PhysicalQubit` 结构体，加入了 $T_2$ 噪声字段。请重构你的优先级比较函数，让 $T_2$ 剩余时间小于 10 微秒的任务直接触发 `QubitDecoherence` 异常。"
2.  **API 仲裁 (Mid-day):**
    * 当 Agent-Delta (写 Python SDK 的) 和 Agent-Alpha (写 Rust 内核的) 在数据结构上产生冲突时，你必须出面决定最终的 Protobuf/JSON 结构，并强制双方遵循。
3.  **Code Review 与集成运行 (Evening):**
    * 拉取所有 Agent 生成的代码合并到主分支。
    * 运行系统级测试：从 Python 端发出一行代码，观察是否能成功穿透 Rust 调度器，最终在 Q-Sim 中输出带有合理误差的测量结果。
    * 如果报错，将错误堆栈 (Error Traceback) 发给对应的 Agent 要求其修复。

## 四、 项目纪律与要求

* **绝对禁止闭门造车:** Agent 生成的所有接口必须先出 API 文档，人类统帅批准后方可写实现代码。
* **内存安全第一:** 内核组 (Agent-Alpha) 必须确保 Rust 代码处于 `#![forbid(unsafe_code)]` 状态下（除了跨语言 FFI 必要部分）。
* **物理常识兜底:** 物理组 (Agent-Gamma) 生成的波形和相干时间参数必须符合当前人类超导量子实验室的公开数据（例如 $T_1$ 在 10-100 微秒区间）。