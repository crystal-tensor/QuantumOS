# Quantum Instruction Set Architecture (QISA) v0.1

**状态**: 草案 (Draft)
**作者**: Agent-Spec (A1)
**日期**: 2026-02-28

## 1. 概述 (Overview)

QISA (Quantum Instruction Set Architecture) 是 QuantumOS 的核心汇编语言。它旨在提供一种低级、显式且具备**时间感知 (Time-Aware)** 能力的指令集，用于直接控制量子处理单元 (QPU)。

与传统高级量子语言不同，QISA 暴露了物理层的时间约束，允许调度器精确控制量子门的执行时机，以最大化保真度并减少退相干错误。

## 2. 数据类型 (Data Types)

*   **q_reg**: 量子寄存器句柄 (例如: `q[0]`, `q[1]`)，映射到物理量子比特。
*   **c_reg**: 经典寄存器句柄 (例如: `c[0]`)，用于存储测量结果 (0 或 1)。
*   **angle**: 浮点数，表示旋转角度 (弧度)。
*   **duration**: 整数，表示时间长度 (纳秒 ns)。

## 3. 核心指令集 (Core Instruction Set)

### 3.1 资源管理 (Resource Management)

#### `QALLOC q_reg`
*   **描述**: 分配一个量子比特，并初始化为 $|0\rangle$ 态。
*   **参数**: `q_reg` - 目标量子寄存器索引。
*   **示例**: `QALLOC q[0]`

#### `QFREE q_reg`
*   **描述**: 释放一个量子比特，将其重置并标记为可用。
*   **参数**: `q_reg` - 目标量子寄存器索引。
*   **示例**: `QFREE q[0]`

### 3.2 量子逻辑门 (Quantum Logic Gates)

#### `U3(theta, phi, lambda) q_reg`
*   **描述**: 单比特通用旋转门。
    $$U3(\theta, \phi, \lambda) = \begin{pmatrix} \cos(\frac{\theta}{2}) & -e^{i\lambda}\sin(\frac{\theta}{2}) \\ e^{i\phi}\sin(\frac{\theta}{2}) & e^{i(\phi+\lambda)}\cos(\frac{\theta}{2}) \end{pmatrix}$$
*   **参数**:
    *   `theta`, `phi`, `lambda`: 欧拉角 (浮点数)。
    *   `q_reg`: 目标量子比特。
*   **示例**: `U3(1.57, 0.0, 3.14) q[0]` (近似 Hadamard 门)

#### `CX q_ctrl, q_target`
*   **描述**: 控制非门 (CNOT)。当控制位 `q_ctrl` 为 $|1\rangle$ 时，翻转 `q_target`。
*   **参数**:
    *   `q_ctrl`: 控制量子比特。
    *   `q_target`: 目标量子比特。
*   **约束**: `q_ctrl` 和 `q_target` 必须物理连接 (参考 DeviceSpec)。
*   **示例**: `CX q[0], q[1]`

### 3.3 测量与反馈 (Measurement & Feedback)

#### `MEASURE q_reg -> c_reg`
*   **描述**: 在 Z 基上测量量子比特，结果存入经典寄存器。
*   **参数**:
    *   `q_reg`: 被测量的量子比特。
    *   `c_reg`: 存储结果的经典比特。
*   **示例**: `MEASURE q[0] -> c[0]`

### 3.4 时序控制 (Timing Control) - **核心特性**

#### `WAIT duration_ns q_reg`
*   **描述**: 强制量子比特 `q_reg` 等待指定的时间长度。在此期间不执行任何门操作，但会发生 $T_1/T_2$ 衰减。
*   **用途**: 用于多比特同步、动态解耦 (Dynamical Decoupling) 序列插入，或模拟特定噪声环境。
*   **参数**:
    *   `duration_ns`: 等待时间 (纳秒)。
    *   `q_reg`: 目标量子比特。
*   **示例**: `WAIT 200 q[0]`

## 4. 示例程序 (Example Program)

```qisa
// Bell State Preparation (Time-Aware)

QALLOC q[0]
QALLOC q[1]

// H on q[0] using U3
U3(1.5708, 0.0, 3.1416) q[0]

// Sync wait to align timing (hypothetical scenario)
WAIT 10 q[1]

// CNOT
CX q[0], q[1]

// Measure
MEASURE q[0] -> c[0]
MEASURE q[1] -> c[1]

QFREE q[0]
QFREE q[1]
```
