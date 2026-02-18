# 40-memory

用于练习多轮对话中的记忆管理。

## 目标

- 维护历史对话上下文
- 控制记忆长度与摘要策略
- 提升多轮对话连贯性

## 记忆种类与验证用例

- 工作记忆（Working Memory / 短期会话记忆）
  - 用例：`validate_working_memory_case.py`
  - 验证点：多轮消息写入、按标记读取、消息数量一致

- 摘要记忆（Compressed Summary Memory）
  - 用例：`validate_summary_memory_case.py`
  - 验证点：压缩摘要 prepend 开关、生效位置与内容正确

- 长期个人记忆（Personal Long-Term Memory）
  - 用例：`validate_personal_long_term_case.py`
  - 验证点：个人偏好/身份信息记录、关键词检索、工具式 record/retrieve

- 长期任务记忆（Task Long-Term Memory）
  - 用例：`validate_task_long_term_case.py`
  - 验证点：任务事项记录、任务关键词检索、工具式 record/retrieve

- 长期工具记忆（Tool Long-Term Memory）
  - 用例：`validate_tool_long_term_case.py`
  - 验证点：工具调用经验记录、报错经验检索、工具式 record/retrieve

## 运行方式

运行全部用例：

```powershell
python main.py
```

单独运行某类记忆用例（示例）：

```powershell
python validate_personal_long_term_case.py
```
