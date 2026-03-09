# QOS 开发状态看板 (TASK_BOARD)

| 任务代号 | 任务描述 | 负责人 | 状态 | 依赖 | 备注 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1-Spec** | 硬件规范 (DeviceSpec) 与 指令集 (QISA) 定义 | Agent-Spec | ✅ 完成 | - | 已通过 Schema 校验 |
| **M1-API** | 通信契约 (API Contract v1) 定义 | Agent-Spec | ✅ 完成 | M1-Spec | 定义了 JobRequest/Response |
| **M2-Kernel** | Rust 内核骨架与调度器 (Scheduler) | Agent-Rust | ✅ 完成 | M1-Spec | 单元测试通过 |
| **M2-HAL** | C++ 硬件抽象层 (Q-HAL) 接口 | Agent-LLVM | ✅ 完成 | M1-Spec | MockDriver 编译通过 |
| **M2-Sim** | Python 数字孪生模拟器 (Q-Sim) | Agent-Phys | ✅ 完成 | M1-Spec | T1/T2 衰减测试通过 |
| **M2-SDK** | Python SDK 装饰器原型 | Agent-SDK | ✅ 完成 | - | JSON 序列化验证通过 |
| **M3-Connect**| Rust 内核集成 Q-HAL | Agent-Rust | ⬜ 待办 | M2-Kernel, M2-HAL | 下一步重点 |
| **M3-Flow** | SDK -> Kernel -> Sim 端到端联调 | All | ⬜ 待办 | All M2 | 里程碑目标 |

## 最近更新
- **2026-02-28**: Agent-Spec 完成了 API Contract v1 定义，解锁了前后端对接标准。
