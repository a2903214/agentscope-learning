# 20-models

用于练习模型配置与切换（不同 provider、不同 model）。

## 目标

- 管理多个模型配置
- 选择默认模型
- 对比不同模型回复效果

## 配置方式

本目录复用全局参数（`src/global_model_config.py`）：

- `OPENAI_BASE_URL`
- `OPENAI_MODEL`（默认模型）
- `OPENAI_API_KEY`
- `DOUBAO_DISABLE_THINKING`（豆包模型可选，`true/false`）

可额外设置备用模型：

- `OPENAI_MODEL_BACKUP`（用于对比）

## 运行

```powershell
python main.py
```

脚本会打印：

- 已加载的两套模型配置（default/backup）
- 选中的默认模型
- 同一问题在两个模型下的回复对比
