# 50-pipeline

用于练习多 Agent 或多步骤编排。

## 目标

- 理解顺序编排（sequential）
- 理解并行分发（fanout）
- 将步骤结果串联为完整流程

## 典型 pipeline 类型（当前实现：6 种）

- 函数式顺序编排：`sequential_pipeline`
- 函数式分发并发：`fanout_pipeline(enable_gather=True)`
- 函数式分发串行：`fanout_pipeline(enable_gather=False)`
- 类式顺序编排：`SequentialPipeline`
- 类式分发并发：`FanoutPipeline(enable_gather=True)`
- 打印流式管道：`stream_printing_messages`

## 每种类型的独立用例文件

- `validate_sequential_function_pipeline.py`
- `validate_fanout_concurrent_pipeline.py`
- `validate_fanout_sequential_pipeline.py`
- `validate_sequential_class_pipeline.py`
- `validate_fanout_class_pipeline.py`
- `validate_stream_printing_pipeline.py`

公共辅助逻辑在 `common.py`，聚合执行入口为 `main.py`。

## 运行方式

运行所有用例：

```powershell
python main.py
```

单独运行某个类型（示例）：

```powershell
python validate_stream_printing_pipeline.py
```
