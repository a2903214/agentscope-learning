# AgentScope 快速使用指南

本指南用于快速完成 AgentScope 的最小可运行示例，帮助你在本地完成从安装到基础对话的闭环。

## 1. 环境准备

- Python 3.10 及以上
- 可用的模型服务 API Key（例如 OpenAI、DashScope 等）

建议先创建虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. 安装依赖

```bash
pip install -U agentscope
```

如需指定模型提供方 SDK，可按需额外安装对应依赖。

## 3. 配置 API Key

以 OpenAI 为例：

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

Linux/macOS:

```bash
export OPENAI_API_KEY="your_api_key"
```

## 4. 最小示例（单 Agent 对话）

创建 `quick_start.py`：

```python
import asyncio
import agentscope
from agentscope.agent import ReActAgent


async def main() -> None:
    agentscope.init(
        model_configs=[
            {
                "config_name": "default_model",
                "model_type": "openai_chat",
                "model_name": "gpt-4o-mini",
                "api_key": "${OPENAI_API_KEY}",
            }
        ],
    )

    agent = ReActAgent(
        name="assistant",
        sys_prompt="你是一个简洁、可靠的技术助手。",
        model_config_name="default_model",
    )

    response = await agent("请用三句话介绍 AgentScope。")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
```

运行：

```bash
python quick_start.py
```

## 5. 常见问题排查

- `401` 或鉴权错误：检查 API Key 是否正确注入环境变量。
- 模型调用失败：确认 `model_type` 与所使用的 provider 配置一致。
- 网络超时：先验证本机网络是否可访问对应模型服务。

## 6. 下一步建议

- 增加工具调用（Toolkit）能力，让 Agent 可执行函数。
- 增加 Memory 与多轮对话，构建会话状态。
- 接入 AgentScope Runtime，将本地 Agent 服务化（SSE/API）。
