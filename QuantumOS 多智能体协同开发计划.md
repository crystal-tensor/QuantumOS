# 基于 OpenClaw 的 QuantumOS (QOS) 多智能体协同开发计划 v3.0

## 一、 OpenClaw 智能体角色配置表

在 OpenClaw 平台中，你需要为每个 QOS 核心模块实例化一个独立的 Agent，并为其分配专属的 System Prompt 与沙盒工具权限。

| 智能体代号 | 核心角色 | OpenClaw 专属 System Prompt 设定 | 赋予的工具权限 (Tools) | 负责代码目录 (Workspace) |
| :--- | :--- | :--- | :--- | :--- |
| **Agent-Spec (A1)** | 架构与规范定义 | 你是 QOS 的顶级架构师。你的唯一输出是 Markdown 规范和 JSON Schema。严格遵循契约驱动设计原则。 | `read_file`, `write_file` | `/docs/spec/` |
| **Agent-Rust (A2)** | 内核与调度器 | 你是顶级 Rust 系统程序员。负责开发非抢占式量子调度器。严格遵守内存安全，禁止使用阻塞线程的代码。 | `rustc`, `cargo_test`, `read_file`, `write_file` | `/kernel_rust/` |
| **Agent-LLVM (A3)** | 编译器与驱动层 | 你是 C++/LLVM 专家。负责将量子指令集 (QISA) 编译为 QIR，并开发底层 HTTP 驱动适配器 (Q-HAL)。 | `clang++`, `make`, `read_file`, `write_file` | `/compiler_llvm/`, `/hal_drivers/` |
| **Agent-Phys (A4)** | 量子物理与模拟 | 你是量子物理学家。负责用 Python 编写注入 $T_1$ 和 $T_2$ 噪声的数字孪生模拟器 (Q-Sim) 以及表面码纠错逻辑。 | `python`, `pytest`, `read_file`, `write_file` | `/q_sim/`, `/qec_engine/` |
| **Agent-SDK (A5)** | API 与开发者生态 | 你是 Python 架构师。负责编写带有高级装饰器的用户 SDK，并处理与 Rust 内核的跨进程序列化通信。 | `python`, `pytest`, `read_file`, `write_file` | `/sdk_python/`, `/api_server/` |

## 二、 OpenClaw 协同工作流设计

多个 OpenClaw Agent 共享同一个项目仓库时，必须建立严格的异步协同机制，由你（总指挥）进行调度。

* **接口先行锁定：** A1 必须首先输出 Schema 或 API 文档。其他所有 Agent 在执行编码任务前，必须调用 `read_file` 读取 A1 的产出，严禁擅自修改数据结构。
* **状态同步看板：** 在根目录维护一个 `TASK_BOARD.md` 文件。每个 Agent 在开始工作前读取该文件获取当前进度，完成后更新状态。
* **自驱闭环测试：** A2-A5 在声称任务完成前，必须通过 OpenClaw 终端调用对应的编译或测试命令（如 `cargo test`）。测试失败时，Agent 需自行读取 Error Log 并重试修复。
* **人工仲裁节点：** 当两个 Agent 出现死循环报错，或对接口定义理解不一致时，OpenClaw 挂起任务，等待你下达明确的仲裁指令。

## 三、 供 OpenClaw 执行的里程碑拆解

将 QOS 的开发拆解解为可供 OpenClaw 直接理解并执行的离散任务包。

### M1: 规范定义与基建库初始化
* 向 **A1** 下达指令：生成 DeviceSpec 的 JSON Schema 和 QISA v0.1 的 Markdown 规范，存入规范目录。
* 向 **A4** 下达指令：根据 A1 的规范，初始化 Python 物理模拟器项目，建立包含 $T_1$ 和 $T_2$ 字段的物理量子比特状态类。

### M2: 核心调度骨架与跨语言通信
* 向 **A2** 下达指令：创建 Rust Cargo 项目，实现一个基于二叉堆的优先级任务队列 (Scheduler) 原型。
* 向 **A5** 下达指令：编写一个 FastAPI 服务，能够将接收到的量子计算任务序列化为标准 JSON 并写入系统队列。
* 向 **A2** 下达指令：配置 Rust 调度器监听该队列，成功解析 A5 传来的 JSON 结构。

### M3: 编译链路与数字孪生闭环
* 向 **A3** 下达指令：编写 C++ LLVM Pass 框架，将基础的量子门操作转化为符合 QIR 标准的中间代码文本。
* 向 **A4** 下达指令：让 Q-Sim 模拟器适配 QIR 指令集，执行含噪的张量网络演化，并返回模拟测量的统计结果。
* **你的验收动作：** 亲自通过 Python SDK 下达一个制备 Bell 态的任务，观察整个系统的数据流转是否顺畅。

## 四、 OpenClaw 标准化指令模板 (Prompt)

在日常指挥中，请直接复制以下模板输入到你的 OpenClaw 对话框中，以确保 Agent 准确领会意图并输出高质量代码。

**【OpenClaw 标准任务分发指令】**
> @[填入目标 Agent，如 Agent-Rust]
> **目标 (Objective):** [一句话描述任务，例如：为 Rust 调度器添加量子比特寿命耗尽的异常处理机制]
> **输入依赖 (Inputs):** 请先读取依赖文件 [填写相对路径，例如：/docs/spec/device_spec.json]
> **输出要求 (Outputs):** 修改对应的源代码文件，并确保逻辑严谨。
> **约束条件 (Constraints):** [例如：不能修改外部被调用的函数签名，必须处理 None 异常]
> **执行与验收要求:** 代码完成后，请自动执行对应的单元测试。如果测试通过，请在 TASK_BOARD.md 中勾选对应任务。如果失败，请分析错误堆栈并自行重试最多 3 次，3 次后向我汇报阻塞点。