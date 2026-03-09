# QuantumOS（QOS）开发计划.md（多 Agent 协同开发版）

> 目标：让你可以**指挥多个 Agent + 你本人**协同推进 QuantumOS（Quantum Runtime OS），并且每个 Agent 都有清晰的职责边界、输入/输出、验收标准与依赖关系。  
> 范围：以“**运行时操作系统**”为主（云/服务器侧），通过 **Q-HAL + Driver 协议**对接不同路线 QPU。  
> 备注：本计划采用“**里程碑 + 进入/退出条件**”组织，避免拍脑袋时间表；你可按团队产能把每个里程碑映射到日历。

---

## 0. 项目总览（一句话）
QOS 是一个**统一 API + 统一 IR + 可插拔硬件驱动（Q-HAL）+ 编译/调度/可复现/审计**的平台，使超导/离子阱/光量子/中性原子等后端以“驱动”形态接入，形成可扩展生态。

---

## 1. 核心原则（所有 Agent 必须遵守）
1. **接口先冻结，再并行实现**：先定 DeviceSpec/QOS-IR/QISA/Driver 协议，再写核心逻辑。
2. **能力表驱动**：上层逻辑只能看 `capabilities/constraints`，禁止硬编码“超导/离子阱分支”。
3. **可复现优先**：任何一次运行都必须可追溯（IR 哈希、设备规格哈希、校准快照、随机种子、run_id）。
4. **幂等与失败可恢复**：`/run` 需幂等键；调度与执行需可重试点设计。
5. **最小可闭环**：先保证 IR→Compile→Run→Result→Artifacts 的端到端闭环，再扩展功能。
6. **测试向量先行**：每个接口/Pass/策略都要配对测试向量（golden cases）。

---

## 2. 交付物清单（Definition of Done）
### 2.1 对外可用的“最小产品”应具备
- Q-HAL：DeviceSpec/Capabilities + Driver 插件体系（本地 + HTTP/JSON）
- Driver 协议：QOS-DP（HTTP/JSON）规范 + 参考实现 + 兼容性测试
- IR：QOS-IR v0（JSON）+ schema + 测试向量
- 编译：Pass pipeline（validate、gateset lowering、layout/routing、noise-aware stub）
- 调度：作业模型 + 状态机 + 策略插件（FIFO/priority）
- API/SDK：提交/查询/运行/获取产物的最小接口
- 可观测：结构化日志、request_id/trace、最小指标
- 审计：append-only 审计记录（最小字段集合）
- 文档：Quickstart、Driver 接入指南、示例用例

---

## 3. 多 Agent 编制与分工（你作为总指挥）
下面给出推荐的 Agent 角色。你可以按你现有机器人数量裁剪合并。

### A0（你本人）— 总指挥 / Chief Architect / 需求与验收
- 决策权：接口冻结、里程碑验收、优先级、对外路线
- 产出：PRD/路线图裁剪、每周验收、对外沟通材料
- 监督：每日站会/周评审，合并策略

### A1 — 架构与规范 Agent（Spec Owner）
- 负责：System Spec、DeviceSpec/QOS-IR/QISA 版本策略、错误码体系、兼容性规则
- 输出：`/docs/spec/*`、schema、golden tests、变更记录（CHANGELOG）
- 依赖：无（最先启动）

### A2 — Driver 协议与参考实现 Agent（Protocol Owner）
- 负责：QOS-DP HTTP/JSON 协议（/spec /compile /run /runs/{id}）的“规范 + 参考实现 + conformance tests”
- 输出：`/drivers/protocol/*`、`/tests/conformance/*`
- 依赖：A1 的版本字段与错误码约定

### A3 — Q-HAL & Driver 适配 Agent（HAL Owner）
- 负责：Q-HAL 接口（Driver API、Registry、HttpDriverAdapter、本地 Driver 规范）
- 输出：`quantumos/qhal/*`、后端注册机制、能力发现与路由策略
- 依赖：A1/A2（协议与 schema）

### A4 — IR & 编译器 Agent（Compiler Owner）
- 负责：QOS-IR 数据结构、Pass 框架与编译产物（artifacts）规范
- 输出：`quantumos/ir/*`、`quantumos/compiler/*`、编译日志与哈希策略
- 依赖：A1（IR schema）、A3（DeviceSpec/Capabilities）

### A5 — Scheduler & Runtime Agent（Runtime Owner）
- 负责：Job 模型、DAG Steps、状态机、策略插件、失败恢复点、执行器骨架
- 输出：`quantumos/scheduler/*`、`quantumos/runtime/*`
- 依赖：A1（作业状态与审计字段）、A3（可用后端列表）

### A6 — API/SDK/CLI Agent（Developer Experience Owner）
- 负责：HTTP API（Runtime 对外）、Python SDK、CLI、示例与教程
- 输出：`quantumos/api.py`（后续可拆服务）、`quantumos/sdk/*`、`examples/*`
- 依赖：A5（runtime 调用）、A4（编译产物格式）

### A7 — Observability & Security Agent（Platform Guard）
- 负责：日志/指标/trace、审计日志结构、鉴权/租户隔离建议、mTLS 部署建议
- 输出：`/docs/ops/*`、日志字段规范、审计落库策略、威胁模型清单
- 依赖：A1（审计字段）、A6（API 鉴权点）

### A8 — QA/CI/Release Agent（Quality Owner）
- 负责：CI（lint/type/test）、回归测试、基准、发布流程（版本号、打包）
- 输出：`.github/workflows/*`、`tests/*`、release checklist
- 依赖：所有模块的测试入口

> **裁剪建议**：如果你机器人不多，可以合并 A2+A3、A4+A5、A7+A8。

---

## 4. 协同开发机制（你用来“指挥机器人”的方法）
### 4.1 统一工单格式（每个任务必须包含）
- **Objective**：要解决什么问题
- **Inputs**：依赖哪些 spec/文件/接口
- **Outputs**：必须产出哪些文件/接口/测试
- **Constraints**：版本/风格/兼容性/不得改动项
- **Acceptance Criteria**：如何判定完成（可运行/测试通过/示例能跑）
- **PR Checklist**：自检项

### 4.2 分支与合并策略（强制）
- 每个 Agent 每个任务一个分支：`agent/<name>/<topic>`
- PR 必须：
  - 通过 CI（lint + type + unit tests）
  - 至少 1 个 reviewer（你或指定 Agent）
  - 更新对应 docs（规范/README/示例）
- 主分支永远可运行（可演示）

### 4.3 代码规范（建议）
- Python：ruff + mypy + pytest
- 日志：结构化 JSON（至少包含 request_id、tenant、job_id、run_id）
- 错误：统一错误码 + `retryable` 标记（对 Driver 协议尤重要）

### 4.4 每日节奏（你来监督）
- “今日目标”同步：每个 Agent 用 5 行文字汇报
- “阻塞点”必须显式列出（依赖哪个 spec/人）
- “可合并产物”优先合并（小步快跑）

---

## 5. 里程碑计划（按“进入/退出条件”推进）
> 你按产能把每个里程碑映射到日历；里程碑不通过，禁止大规模并行扩张。

### M0 — 项目治理与仓库基建（Bootstrap）
**进入条件**：仓库已创建（已有 skeleton）  
**退出条件**：
- LICENSE（建议 Apache-2.0）/ CODEOWNERS / CONTRIBUTING
- CI：lint/type/test 基础跑通
- docs 目录结构建立：`docs/spec`, `docs/ops`, `docs/dev`
- Issue/PR 模板（任务包格式）

### M1 — 接口冻结（最关键）
**退出条件**（全部完成并合入）：
- DeviceSpec schema + version policy
- QOS-IR schema（v0）+ QISA（v0）
- QOS-DP 协议（HTTP/JSON）规范 + 错误码/幂等/重试规则
- golden test vectors（最少：Bell、GHZ、参数门、测量校正用例）

### M2 — 端到端闭环（最小可演示）
**退出条件**：
- `SDK/CLI` 构造 IR → 编译 pipeline → driver.run → 返回 counts
- artifacts 落盘（ir hash、native hash、pass log、calibration_id、seed）
- 本地 simulator driver 可跑；HTTP driver adapter 可跑（对接参考 driver server）

### M3 — 作业系统化（从“单次 run”到“Job DAG”）
**退出条件**：
- Job + DAG steps（classical/quantum）基本可跑
- 状态机完整 + 失败可恢复点（compile 失败、run 失败）
- 调度策略插件（FIFO/priority）+ 基本配额（concurrent/jobs）

### M4 — 可观测与审计（可交付门槛）
**退出条件**：
- API 全链路 request_id/trace 贯通
- 审计日志 append-only（本地文件/轻量 DB 方案皆可）
- 运行结果可追溯：给定 run_id 能找到 IR/设备规格/校准快照/编译产物

### M5 — 真实后端接入（生态启动点）
**退出条件**：
- 接入 1 个真实后端（哪怕门级）：完成 driver 插件 + conformance tests
- 能力表驱动：不改上层即可替换后端运行同一 IR
- 基础误差缓解接口接入（至少测量校正）

### M6 — 多租户/SLA/部署（走向生产）
**退出条件**：
- tenant + quota + rate limit
- 部署指南（mTLS、密钥、日志采集、监控、审计）
- release 版本化与兼容性声明

---

## 6. 详细任务分解（Epic → Stories → 产物）
下面给出“你可以直接复制给机器人”的任务包颗粒度。

### EPIC-1：Spec 与 Schema（A1）
- S1.1 DeviceSpec JSON Schema（含 topology/gates/timing/noise/limits）
- S1.2 QOS-IR v0 schema（module/circuit/op）
- S1.3 QISA v0（门级）规范文档
- S1.4 版本策略与兼容性（0.x → 1.x 规则）
- S1.5 Golden 测试向量（Bell/GHZ/Param/Measure）

**验收**：schema 可验证；每个向量都有期望行为（accept/reject 与错误码）。

### EPIC-2：Driver 协议与一致性测试（A2）
- S2.1 QOS-DP 协议文档（headers、idempotency、retry、errors）
- S2.2 参考 driver server（/health /spec /compile /run /runs/{id}）
- S2.3 Conformance test runner：对任意 driver base_url 跑一套测试
- S2.4 错误码映射与 retryable 规则落地

**验收**：参考 server 通过 conformance；任意新 driver 接入必须先过 conformance。

### EPIC-3：Q-HAL & HttpDriverAdapter（A3）
- S3.1 Q-HAL Driver 抽象（已存在）
- S3.2 HttpDriverAdapter（已加入）
- S3.3 Spec cache/TTL、compile 缓存策略、运行幂等键注入策略
- S3.4 多 backend registry 与路由（按 capability 选择）

**验收**：能一行切换 backend（sim ↔ http ↔ real），上层无改动。

### EPIC-4：Compiler Pipeline（A4）
- S4.1 Pass 框架与 pass log 规范
- S4.2 ValidatePass（严格 schema 与 capability 校验）
- S4.3 GateSetLoweringPass（最少支持：常见门分解）
- S4.4 LayoutRoutingPass（耦合图插 SWAP，先朴素算法）
- S4.5 NoiseAwareOptimizePass（先 stub + hooks）

**验收**：给定设备 native_gates/coupling_map 能产出可运行 IR；pass log 与 artifacts 完整。

### EPIC-5：Scheduler/Runtime（A5）
- S5.1 Job/DAG 模型（已存在骨架）
- S5.2 状态机与可恢复点（失败分类）
- S5.3 策略插件：FIFO/priority/EDF stub
- S5.4 执行器：取队列 → 编译 → run → 写回结果
- S5.5 资源模型：concurrency、shots budget、backend availability

**验收**：提交 Job（含多个 steps）可跑通并产出完整记录；失败可重试且幂等。

### EPIC-6：API/SDK/CLI（A6）
- S6.1 HTTP API：/submit_job /job/{id} /cancel /backends /run_simple
- S6.2 SDK：Python client + typed models
- S6.3 CLI：run、submit、status、download-artifacts
- S6.4 Examples：最少 3 个（sim、http、job DAG）

**验收**：用户可不看代码完成一次运行与结果获取；文档可复现。

### EPIC-7：Observability/Security/Audit（A7）
- S7.1 结构化日志规范（字段表）
- S7.2 request_id/trace 贯通（API→runtime→driver）
- S7.3 审计日志结构（append-only）与落库建议
- S7.4 鉴权/租户隔离设计（token claims、mTLS 建议）

**验收**：任意 run_id 可追溯到完整输入/产物；安全方案可落地部署。

### EPIC-8：QA/CI/Release（A8）
- S8.1 CI：ruff/mypy/pytest
- S8.2 合同测试：driver conformance + ir schema validate
- S8.3 回归集：典型电路 + 策略 + 失败场景
- S8.4 Release checklist：版本号、兼容性声明、迁移指南

**验收**：每次合并主分支自动跑完测试；release 可重复。

---

## 7. 依赖关系（文本版）
- M1（接口冻结）是所有并行工作的前置依赖
- Compiler（A4）依赖 DeviceSpec/IR（A1）与 capabilities（A3）
- Scheduler/Runtime（A5）依赖 JobSpec（A1）与 backend registry（A3）
- API/SDK（A6）依赖 Runtime（A5）与 artifacts（A4）
- Observability（A7）贯穿全部，需最早介入定义字段
- QA（A8）需要在 M0 即搭好 CI，并在 M1 后补 conformance 测试

---

## 8. 你作为总指挥的“监督面板”（每天只看这些就够）
1. **接口变更数**：schema/协议是否仍在频繁动？（若是，先冻结）
2. **主分支是否可演示**：CLI/Example 是否还能一键跑通？
3. **Conformance 测试是否全绿**：任何 driver 接入必须先绿
4. **可复现要素是否齐全**：run_id 是否能定位 IR/spec/calibration/seed？
5. **阻塞列表**：哪个 Agent 被谁阻塞？（你来解锁）

---

## 9. 给 Agent 的“任务指令模板”（你直接复制粘贴）
**任务包：<TASK_ID> <标题>**
- Objective：  
- Inputs（链接/文件/接口）：  
- Outputs（必须新增/修改的文件列表）：  
- Constraints（版本、不得改动项、兼容性要求）：  
- Acceptance Criteria（可运行命令、测试项、截图/日志证据）：  
- PR Checklist：  
  - [ ] 单元测试/合同测试通过  
  - [ ] 文档更新（docs/README/examples）  
  - [ ] 不破坏主分支演示  
  - [ ] 关键接口含版本字段与错误码  

---

## 10. 附：建议目录结构（长期演进）
- `docs/spec/`：系统规范（DeviceSpec/QOS-IR/QISA/QOS-DP）
- `docs/dev/`：开发指南（如何写 driver、如何写 pass、如何写 policy）
- `docs/ops/`：部署与运维（mTLS、监控、审计）
- `drivers/`：参考 driver/协议工具/一致性测试
- `quantumos/`：核心 runtime
- `tests/`：schema、conformance、回归
