# 30-tools

用于练习 Toolkit 的工具类型与注册/调用验证。

## 目标

- 编写可被 Agent 调用的函数
- 组织工具输入输出
- 在对话中触发工具调用

## Tool 类型清单（AgentScope Toolkit）

- Function Tool（函数工具）
  - 同步函数工具
  - 异步函数工具
  - 流式输出工具
  - 预设参数工具（`preset_kwargs`）
  - 后处理工具（`postprocess_func`）
  - 自定义 Schema 工具（`json_schema`）
- Tool Group（工具分组与激活控制）
- Agent Skill（`register_agent_skill`，基于 `SKILL.md`）
- MCP Tool（`register_mcp_client`，外部 MCP 服务工具）
- Middleware Tool（`register_middleware`，工具调用链路中间件）

## 本目录已实现的验证

每种验证已拆分为独立文件：

- `validate_sync_tool.py`
- `validate_async_tool.py`
- `validate_stream_tool.py`
- `validate_group_activation.py`
- `validate_preset_kwargs_tool.py`
- `validate_postprocess_tool.py`
- `validate_custom_schema_tool.py`
- `validate_agent_skill_tool.py`
- `validate_mcp_tool.py`
- `validate_llm_tool_invocation.py`

公共逻辑在 `common.py`，聚合执行入口仍为 `main.py`。

其中 `validate_llm_tool_invocation.py` 会做真实大模型验证：

- 确认 LLM 在 ReAct 流程中确实调用了工具
- 确认工具入参与返回值正确
- 确认最终回复包含工具返回结果

## 同步 vs 异步验证差异

- `validate_sync_tool.py`
  - 使用阻塞型工具 `add_blocking`（内部 `time.sleep`）
  - 并发发起 3 次调用，但总耗时接近串行（约 `0.6s`）
- `validate_async_tool.py`
  - 使用非阻塞工具 `reverse_text_nonblocking`（内部 `await asyncio.sleep`）
  - 并发发起 3 次调用，总耗时接近单次延时（约 `0.2s`）

## 运行方式

```powershell
python main.py
```

也可以单独运行任意验证文件，例如：

```powershell
python validate_mcp_tool.py
```

> `validate_llm_tool_invocation.py` 需要可用模型配置（`.env` 中的 `OPENAI_*` 参数）和网络连通性。

成功时会输出 `=== ALL TOOL VALIDATIONS PASSED ===`。
