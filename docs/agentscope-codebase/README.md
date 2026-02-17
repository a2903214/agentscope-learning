# AgentScope 设计文档（本地编制版）

本目录为基于本地代码与仓库文档阅读后编制的设计文档集合，覆盖以下项目：

- AgentScope（`s:\agentscope\agentscope-codebase\agentscope`）
- AgentScope Runtime（`s:\agentscope\agentscope-codebase\agentscope-runtime`）
- AgentScope Studio（`s:\agentscope\agentscope-codebase\agentscope-studio`）
- AgentScope Spark Design（`s:\agentscope\agentscope-codebase\agentscope-spark-design`）
- AgentScope Samples（`s:\agentscope\agentscope-codebase\agentscope-samples`）

## 目录结构

- `00-overall-design/`
  - `overall_design.zh-CN.md`：跨项目总体架构、边界、关键集成点
  - `core_module_design.zh-CN.md`：跨项目核心模块与关键流程（含时序图）
- `10-agentscope/`：AgentScope 框架侧设计文档
- `20-agentscope-runtime/`：Runtime（Agent-as-a-Service、Sandbox、Deploy、Tracing）设计文档
- `30-agentscope-studio/`：Studio（Server/Client、OTel、Socket、DB）设计文档
- `40-agentscope-spark-design/`：Spark Design（组件库、构建发布、文档站）设计文档
- `50-agentscope-samples/`：Samples（示例组织方式、纯 Python 与 fullstack runtime 范式）设计文档

## 命名规范

- 文件名统一使用英文小写下划线（snake_case）。
- 语言后缀采用 BCP-47 风格：`.<lang>.md`，例如：`overall_design.zh-CN.md`、`core_module_design.en.md`。
- 文件夹统一使用 `NN-kebab-case`（两位序号 + 英文短横线命名），例如：`00-overall-design`、`10-agentscope`。

## 阅读入口（建议顺序）

1. `00-overall-design/overall_design.zh-CN.md`
2. `00-overall-design/core_module_design.zh-CN.md`
3. 按需进入各项目目录（`10-` 到 `50-`）中的 `overall_design.zh-CN.md` 与 `core_module_design.zh-CN.md`

## 文档清单（按项目）

- **跨项目**
  - `00-overall-design/overall_design.zh-CN.md`
  - `00-overall-design/core_module_design.zh-CN.md`
- **AgentScope**
  - `10-agentscope/overall_design.zh-CN.md`
  - `10-agentscope/core_module_design.zh-CN.md`
- **AgentScope Runtime**
  - `20-agentscope-runtime/overall_design.zh-CN.md`
  - `20-agentscope-runtime/core_module_design.zh-CN.md`
- **AgentScope Studio**
  - `30-agentscope-studio/overall_design.zh-CN.md`
  - `30-agentscope-studio/core_module_design.zh-CN.md`
- **AgentScope Spark Design**
  - `40-agentscope-spark-design/overall_design.zh-CN.md`
  - `40-agentscope-spark-design/core_module_design.zh-CN.md`
- **AgentScope Samples**
  - `50-agentscope-samples/overall_design.zh-CN.md`
  - `50-agentscope-samples/core_module_design.zh-CN.md`

