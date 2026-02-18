# 10-hello-agentscope

最小可运行 AgentScope 示例目录。

## 目标

- 完成 AgentScope 初始化
- 创建一个基础 Agent
- 发起一次简单对话

## 运行前提

- 已安装 `agentscope`
- 已设置豆包 API Key（使用 OpenAI 兼容模式）

PowerShell 示例：

```powershell
$env:OPENAI_API_KEY="your_doubao_api_key"
$env:OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
$env:OPENAI_MODEL="doubao-1.5-pro-32k-250115"
python main.py
```

说明：

- `OPENAI_BASE_URL` 和 `OPENAI_MODEL` 不设置时，脚本默认使用豆包的上述配置。
- 全局参数统一定义在 `src/global_model_config.py`，本目录脚本会直接复用。

## 通过标准

脚本输出 `PASS: AgentScope hello validation succeeded.` 即表示：

- AgentScope 初始化成功
- Agent 创建成功
- 模型调用链路可用
