# 00-environment

用于完成本地开发环境初始化与验证。

## 目标

- 创建并激活 Python 虚拟环境
- 安装 AgentScope
- 验证 Python 与依赖是否可用

## 建议步骤

1. 创建虚拟环境
2. 安装依赖
3. 运行 `main.py` 做环境检查

## 验证内容

`main.py` 会执行以下检查：

- Python 版本是否满足 `>= 3.10`
- `agentscope` 包是否可导入
- 核心模块是否可导入（`agent/message/pipeline/tool`）
- 是否检测到常见模型 API Key（仅提示，不阻断）

运行命令：

```bash
python main.py
```

如果最后输出 `PASS : AgentScope environment is ready.`，说明环境验证通过。
