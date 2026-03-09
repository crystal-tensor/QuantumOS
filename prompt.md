喂给 Agent-Spec (A1) 的首发指令
核心任务：起草全局法典（DeviceSpec 与 QISA）

Markdown
@Agent-Spec
**目标 (Objective):** 作为 QOS 的首席规范定义者，你需要完成项目的“冷启动”。请起草量子硬件设备能力规范（DeviceSpec）的 JSON Schema，以及量子指令集（QISA）的初始文档。
**输入依赖 (Inputs):** 无。你是整个生态的上游起点。
**输出要求 (Outputs):**
1. 创建文件 `/docs/spec/device_spec_v0.json` (定义包含拓扑结构、门保真度、$T_1$、$T_2$ 寿命限制的 JSON Schema)。
2. 创建文件 `/docs/spec/qisa_v0.md` (定义 QALLOC, QFREE, MEASURE, U3, CX, WAIT 等核心量子汇编指令)。
**约束条件 (Constraints):** 1. JSON Schema 必须符合 Draft 7 或更新标准，必须包含严格的类型校验。
2. QISA 指令集必须体现出“时间感知（Time-aware）”的特性，这是 QOS 的核心壁垒。
**执行与验收要求:** 文件生成完毕后，请使用 Python 的 `jsonschema` 库编写一个简单的校验脚本，自我验证你写的 JSON Schema 格式是否合法。成功后在终端输出“M1-Spec 规范初始化完成”。
2. 喂给 Agent-Rust (A2) 的首发指令
核心任务：根据规范，搭建 Rust 内核骨架

Markdown
@Agent-Rust
**目标 (Objective):** 作为内核程序员，你需要初始化 QOS 的 Rust 核心项目，并根据 A1 刚刚制定的 DeviceSpec 规范，用 Rust 定义出物理量子比特的内存数据结构。
**输入依赖 (Inputs):** 请使用 `read_file` 读取 `/docs/spec/device_spec_v0.json`。
**输出要求 (Outputs):**
1. 在 `/kernel_rust/` 目录下执行 `cargo init --lib`。
2. 创建 `src/qubit.rs`，定义 `PhysicalQubit` 结构体，必须精确映射 DeviceSpec 中的 $T_1$（弛豫时间）、$T_2$（退相干时间）和门保真度参数。
3. 创建 `src/scheduler.rs`，定义一个基于 `BinaryHeap` 的基础任务队列（Scheduler）骨架。
**约束条件 (Constraints):** 1. 绝对禁止使用 `unsafe` 块。
2. 所有时间单位在 Rust 内部强制统一使用 `u64` 表示的纳秒（ns）。
**执行与验收要求:** 编写 unit tests 验证 `PhysicalQubit` 的实例化。执行 `cargo test`。如果编译报错或测试失败，请自行分析 Rust 编译器的提示并修复。测试全绿后汇报。
3. 喂给 Agent-LLVM (A3) 的首发指令
核心任务：定义 C++ 硬件抽象层 (Q-HAL) 接口

Markdown
@Agent-LLVM
**目标 (Objective):** 作为编译器与底层驱动专家，你需要初始化 C++ 驱动工程，并定义出 Q-HAL（量子硬件抽象层）的纯虚类接口，为后续对接超导和离子阱硬件做好准备。
**输入依赖 (Inputs):** 请使用 `read_file` 读取 `/docs/spec/qisa_v0.md`，理解我们需要支持哪些基础量子门。
**输出要求 (Outputs):**
1. 在 `/hal_drivers/` 目录下创建 `CMakeLists.txt`。
2. 创建头文件 `include/qhal_driver.hpp`。
3. 在头文件中定义一个抽象基类 `IQHalDriver`，包含如 `allocate_qubit()`, `execute_u3(qubit_id, theta, phi, lambda)`, `execute_wait(qubit_id, duration_ns)` 等纯虚函数。
**约束条件 (Constraints):** 1. 使用现代 C++ (C++17 或以上) 标准。
2. 接口设计必须解耦，Driver 层只负责接收标准指令，不负责业务调度逻辑。
**执行与验收要求:** 编写一个最简单的 MockDriver 子类实现这些接口（打印日志即可），并通过 CMake 编译出一个静态库。执行 `make` 成功后汇报。
4. 喂给 Agent-Phys (A4) 的首发指令
核心任务：构建 Python 数字孪生模拟器底座

Markdown
@Agent-Phys
**目标 (Objective):** 作为量子物理学家，你需要搭建 Q-Sim 数字孪生模拟器的基础框架。这不是一个完美的数学模拟器，而是一个必须包含“时间流逝”和“物理退相干噪声”的真实感模拟器。
**输入依赖 (Inputs):** 请使用 `read_file` 读取 `/docs/spec/device_spec_v0.json`。
**输出要求 (Outputs):**
1. 在 `/q_sim/` 目录下初始化 Python 环境（生成 `requirements.txt`，包含 `numpy`, `scipy`）。
2. 创建 `virtual_backend.py`。定义 `VirtualQubit` 类。
3. 实现一个核心函数 `apply_idle_noise(duration_ns)`：当量子比特闲置时，根据 $T_1$ 和 $T_2$ 公式，计算并应用指数衰减的噪声（产生状态的坍缩或保真度下降）。
**约束条件 (Constraints):** 纯净的代码结构，必须对外部（特别是 Rust 内核）提供清晰的 Python API 以便后续被调用。
**执行与验收要求:** 使用 `pytest` 编写测试用例：初始化一个处于叠加态的虚拟量子比特，让其等待超过 $T_2$ 时间，断言其保真度显著下降。测试通过后汇报。
5. 喂给 Agent-SDK (A5) 的首发指令
核心任务：开发 Python 用户端 API 装饰器

Markdown
@Agent-SDK
**目标 (Objective):** 作为开发者体验架构师，你需要为最终用户（算法研究员）提供极其优雅的编程接口。你需要建立 SDK 的基础结构，并实现将高层代码打包序列化的能力。
**输入依赖 (Inputs):** 了解我们要建立的是类似 Python 发送 JSON 给 Rust 内核的架构。
**输出要求 (Outputs):**
1. 在 `/sdk_python/` 目录下初始化项目。
2. 创建 `spectrum_os/core.py`。
3. 实现核心装饰器 `@quantum_task(required_qubits, expected_time_ns)`。
4. 当前阶段，该装饰器的功能是：拦截用户定义的函数，并将其转化为一个包含 Job 元数据的标准 JSON payload（暂不涉及真实的语法树解析）。
**约束条件 (Constraints):** 生成的 JSON payload 格式必须具有极强的扩展性，包含 `job_id`, `tenant`, `resources_req` 等必须字段。
**执行与验收要求:** 编写一个 `example.py`，使用你写的 `@quantum_task` 装饰一个简单的 Python 函数，运行该脚本并成功在控制台打印出被拦截生成的结构化 JSON 字符串。完成后汇报。
下一步建议