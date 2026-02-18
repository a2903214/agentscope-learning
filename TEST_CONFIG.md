# 用例测试配置说明

`agentscope-learning/src` 下各章节用例的快速执行方式与默认参数说明。

## 0. Test Explorer 视窗中显示用例

已用 **pytest** 将各章节入口包装为可发现用例，Test Explorer 会显示 8 条用例：

- `test_00_environment` — 00-environment 环境校验  
- `test_10_hello_agentscope` — 10-hello-agentscope  
- `test_20_models` — 20-models  
- `test_30_tools_all` — 30-tools 全部工具用例  
- `test_40_memory_all` — 40-memory 全部记忆用例  
- `test_50_pipeline_all` — 50-pipeline 全部编排用例  
- `test_60_runtime_all` — 60-runtime 全部运行时用例  
- `test_70_examples_default_args` — 70-examples（默认参数）

**操作**：侧边栏打开 **Testing (测试)**，若未发现用例，点击刷新图标或执行 **Python: Discover Tests**。  
**依赖**：需安装 `pytest`（`pip install pytest`）。  
**配置**：工作区根为 `s:\agentscope` 时，已在 `.vscode/settings.json` 中设置 `python.testing.cwd` 为 `agentscope-learning`，pytest 从该目录发现 `tests/` 下用例。

## 1. 使用 VS Code / Cursor 运行

在项目根目录打开工作区（`s:\agentscope`）时，使用 **运行和调试** 下拉选择对应配置即可：

| 配置名称 | 说明 |
|----------|------|
| **00-environment (环境校验)** | 检查 Python、AgentScope 及模型 API Key |
| **10-hello-agentscope** | 简单 Agent 调用校验 |
| **20-models** | 多模型配置对比（可选环境变量见下） |
| **30-tools (全部工具用例)** | 同步/异步/流式/MCP/Skill 等工具用例 |
| **40-memory (全部记忆用例)** | 工作记忆、摘要、长期记忆等用例 |
| **50-pipeline (全部编排用例)** | 顺序/扇出/流式打印等编排用例 |
| **60-runtime (全部运行时用例)** | 阶段、沙箱、端到端运行时用例 |
| **70-examples (股票热点分析，默认参数)** | 热点驱动投资分析，使用下方默认参数 |

配置文件位置：`agentscope-learning/.vscode/launch.json`。  
若工作区是 `agentscope-learning`，请将 `launch.json` 中的 `${workspaceFolder}` 视为 `agentscope-learning`，即 `program`/`cwd` 中的路径去掉一层 `agentscope-learning/`（例如 `program` 改为 `"${workspaceFolder}/src/00-environment/main.py"`，`cwd` 改为 `"${workspaceFolder}/src"`）。

## 2. 命令行运行

**统一约定**：从 `agentscope-learning/src` 目录执行，以便正确加载 `_bootstrap_agentscope_codebase` 与 `global_model_config`。

```bash
cd agentscope-learning/src
python 00-environment/main.py
python 10-hello-agentscope/main.py
python 20-models/main.py
python 30-tools/main.py
python 40-memory/main.py
python 50-pipeline/main.py
python 60-runtime/main.py
python 70-examples/main.py --topic AI算力 --horizon 中期 --risk 中等
```

## 3. 各用例入口与默认参数

| 目录 | 入口 | 默认参数 | 说明 |
|------|------|----------|------|
| `00-environment` | `main.py` | 无 | 环境与依赖校验 |
| `10-hello-agentscope` | `main.py` | 无 | Hello AgentScope 校验 |
| `20-models` | `main.py` | 无 | 模型对比；可选环境变量 `OPENAI_MODEL_BACKUP` 指定备用模型 |
| `30-tools` | `main.py` | 无 | 一次性跑完本目录所有 `validate_*.py` 工具用例 |
| `40-memory` | `main.py` | 无 | 一次性跑完本目录所有记忆用例 |
| `50-pipeline` | `main.py` | 无 | 一次性跑完本目录所有编排用例 |
| `60-runtime` | `main.py` | 无 | 一次性跑完本目录所有运行时用例 |
| `70-examples` | `main.py` | 见下 | 股票热点主题投资分析（LLM 驱动） |

### 70-examples 默认参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--topic` | `AI算力` | 热点主题偏好 |
| `--horizon` | `中期` | 投资期限 |
| `--risk` | `中等` | 风险偏好 |

示例：自定义运行

```bash
cd agentscope-learning/src
python 70-examples/main.py --topic 低空经济 --horizon 短期 --risk 保守
```

## 4. 单独运行子用例（validate_*.py）

若需只跑某一类用例，可在 `agentscope-learning/src` 下执行对应脚本（无需参数）：

- **30-tools**：`python 30-tools/validate_sync_tool.py`、`validate_async_tool.py`、`validate_stream_tool.py`、`validate_group_activation.py`、`validate_preset_kwargs_tool.py`、`validate_postprocess_tool.py`、`validate_custom_schema_tool.py`、`validate_agent_skill_tool.py`、`validate_mcp_tool.py`、`validate_llm_tool_invocation.py`
- **40-memory**：`python 40-memory/validate_working_memory_case.py`、`validate_summary_memory_case.py`、`validate_personal_long_term_case.py`、`validate_task_long_term_case.py`、`validate_tool_long_term_case.py`
- **50-pipeline**：`python 50-pipeline/validate_sequential_function_pipeline.py`、`validate_fanout_concurrent_pipeline.py`、`validate_fanout_sequential_pipeline.py`、`validate_sequential_class_pipeline.py`、`validate_fanout_class_pipeline.py`、`validate_stream_printing_pipeline.py`
- **60-runtime**：`python 60-runtime/validate_flow_stage_cases.py`、`validate_sandbox_cases.py`、`validate_end_to_end_runtime_case.py`

## 5. 环境与密钥

- 运行前确保已安装 AgentScope 并配置本地代码库（见 `_bootstrap_agentscope_codebase.py`）。
- 多数用例依赖模型 API，请在 `.env` 或环境中配置至少一个：`OPENAI_API_KEY`、`DASHSCOPE_API_KEY`、`ANTHROPIC_API_KEY`、`GOOGLE_API_KEY` 等（参见 `00-environment/main.py` 与 `global_model_config.py`）。
