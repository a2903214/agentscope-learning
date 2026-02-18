# 60-runtime

用于练习将 Agent 服务化（`agentscope-runtime` + `/process` API + SSE）。

## 目标

- 理解 Agent-as-a-Service 基本流程
- 运行最小服务并接收请求
- 观察事件流输出

## Agent-as-a-Service 基本流程（基于 `agentscope-runtime` 接口）

- 请求接入：`request_received`
- 鉴权校验：`auth_checked`
- 会话装载：`session_loaded`
- Agent 规划：`agent_planned`
- 沙箱执行：`sandbox_selected -> sandbox_establishing -> sandbox_established -> sandbox_health_checked -> sandbox_started -> sandbox_succeeded`
- 响应回传：`response_streaming -> response_completed`

以上阶段由 `AgentApp` 的 `@query(framework="agentscope")` 处理，并通过 `/process` SSE 输出。
本目录用例会真实启动 `AgentApp` 进程，再通过 HTTP 请求触发执行。
其中 `local_python`、`mcp`、`docker` 均会尝试真实启动（子进程/容器）。

## 用例设计

- 流程环节用例：`validate_flow_stage_cases.py`
  - 目标：验证 AaaS 各环节事件是否齐全且顺序正确
  - 校验点：通过 `/process` SSE 读取事件，验证关键阶段全部出现、顺序满足约束

- 沙箱类型用例：`validate_sandbox_cases.py`
  - 目标：对各类沙箱分别验证
  - 覆盖：`local_python`、`docker`、`mcp`
  - 校验点：沙箱真实建立/执行结果是否匹配、事件流是否合理

- 完整端到端用例：`validate_end_to_end_runtime_case.py`
  - 目标：在单次完整流程中串行执行多类沙箱并收敛结果
  - 校验点：三类沙箱是否全部覆盖且顺序正确、最终响应是否完成、事件守卫是否能识别异常流

## 事件合理性检查

事件校验在 `common.py` 中统一实现（事件来自 `/process` SSE）：

- 连续性：`seq` 必须连续递增
- 一致性：`trace_id` 在同次请求内保持不变
- 时序性：时间戳单调不回退
- 结构性：首事件必须是 `request_received`，尾事件必须是 `response_completed`
- 生命周期完整性：每个 `sandbox_started` 必须匹配对应的 `sandbox_succeeded`
- 建立有效性：每个沙箱必须先完成 `sandbox_established` 与 `sandbox_health_checked`
- 不可用处理：当真实环境不可用（例如 Docker daemon 未启动）时，必须产生 `sandbox_unavailable`（`status=skipped`）且附带原因
- 全流程覆盖（E2E）：必须包含 `local_python/docker/mcp` 三类沙箱

同时提供“异常流探测”校验：故意构造损坏事件流，确认守卫能正确报错。

## 运行方式

运行全部用例：

```powershell
python main.py
```

单独运行某类用例（示例）：

```powershell
python validate_end_to_end_runtime_case.py
```
