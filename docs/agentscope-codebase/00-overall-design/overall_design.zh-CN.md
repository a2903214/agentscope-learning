# 总体设计（跨项目）

## 1. 背景与目标

AgentScope 生态由「框架（AgentScope）+ 运行时（AgentScope Runtime）+ 可视化（Studio）+ UI 组件库（Spark Design）+ 示例（Samples）」组成，目标是以可扩展的抽象构建智能体应用，并在生产环境中提供可部署、可观测、可迭代的运行闭环。

## 2. 系统边界与组件划分

### 2.1 逻辑组件

- **AgentScope（框架）**：提供 Agent 抽象、消息类型、模型适配、工具调用、记忆、pipeline 等能力。
  - 代表实现：`ReActAgent`（`agentscope-codebase/agentscope/src/agentscope/agent/_react_agent.py`）、`Toolkit`（`.../tool/_toolkit.py`）、`stream_printing_messages`（`.../pipeline/_functional.py`）。
- **AgentScope Runtime（运行时/部署）**：提供 Agent-as-a-Service（FastAPI）、协议适配（A2A/Response API/AGUI）、会话/中断、Sandbox 安全工具执行、部署管理、Tracing（OTel/日志）。
  - 代表实现：`AgentApp`（`agentscope-codebase/agentscope-runtime/src/agentscope_runtime/engine/app/agent_app.py`）、`Runner`（`.../engine/runner.py`）、`SandboxManager`（`.../sandbox/manager/sandbox_manager.py`）。
- **AgentScope Studio（本地可视化）**：本地 server + client，用于项目与运行管理、消息可视化、Tracing/评测等；支持 OTEL gRPC/HTTP 接收链路与 Socket.IO 实时推送。
  - 代表实现：server 启动（`agentscope-codebase/agentscope-studio/packages/server/src/index.ts`）、DB（`.../database.ts`）、Socket（`.../trpc/socket.ts`）。
- **Spark Design（UI 组件库）**：`@agentscope-ai/design`（通用组件/主题/i18n）与 `@agentscope-ai/chat`（聊天组件），用于构建 AI 交互 UI（Studio/Samples 可复用）。
  - 仓库结构见 `agentscope-codebase/agentscope-spark-design/README.md`。
- **Samples（示例）**：以“功能/场景”为组织方式，提供纯 Python 与 fullstack runtime 示例（前后端 + Runtime）供参考落地。
  - 结构见 `agentscope-codebase/agentscope-samples/README.md`。

### 2.2 物理部署视角（典型）

- **纯本地**：Python 应用直接调用 AgentScope（无 Runtime、无 Studio）。
- **本地服务化**：Runtime 启动 FastAPI 对外提供 SSE/协议 API；可选接入 Studio 做可视化与追踪。
- **生产化**：Runtime + Sandbox（Docker/K8s）+ 可观测（OTel）+（可选）Studio/自研 UI。

### 2.3 各项目代码结构概览

| 项目 | 代码根路径 | 主要目录/包结构 |
|------|------------|-----------------|
| **agentscope** | `agentscope-codebase/agentscope/src/agentscope/` | `agent/`、`message/`、`model/`、`formatter/`、`tool/`、`pipeline/`、`memory/`、`session/`、`rag/`、`evaluate/`、`tune/`、`tracing/`、`mcp/`、`a2a/`、`plan/`、`realtime/`、`tts/` 等 |
| **agentscope-runtime** | `agentscope-codebase/agentscope-runtime/src/agentscope_runtime/` | `engine/`（app、runner、deployers、tracing）、`sandbox/`（manager、box）、`adapters/`、`tools/`（generations、searches、realtime_clients 等） |
| **agentscope-studio** | `agentscope-codebase/agentscope-studio/packages/` | `server/`（Express、TRPC、Socket、DB、otel）、`client/`（Vite/React） |
| **agentscope-spark-design** | `agentscope-codebase/agentscope-spark-design/packages/` | `spark-design/`（antd、components、hooks、libs、i18n）、`spark-chat/`（Bubble、Sender、Markdown、Mermaid、Conversations 等） |
| **agentscope-samples** | `agentscope-codebase/agentscope-samples/` | 按场景：`alias/`、`browser_use/`、`deep_research/`、`conversational_agents/`、`evaluation/`、`tuner/`、`evotraders/` 等 |

## 3. 技术架构框图

```mermaid
flowchart TB
  subgraph 用户与前端
    User[用户/业务系统]
    UI[Studio Client / 自研 UI]
    UI --> User
  end

  subgraph agentscope-studio["agentscope-studio"]
    ST_Server[server: Express+TRPC+OTEL+Socket]
    ST_Client[client: Vite/React]
    ST_DB[(TypeORM DB)]
    ST_Server --> ST_DB
    ST_Client --> ST_Server
  end

  subgraph agentscope-runtime["agentscope-runtime"]
    AgentApp[engine::AgentApp FastAPI]
    Runner[engine::Runner]
    Deploy[engine::DeployManager]
    Sandbox[sandbox::SandboxManager]
    Tracing[engine::tracing]
    AgentApp --> Runner
    Runner --> Deploy
    Runner --> Sandbox
    Runner --> Tracing
  end

  subgraph agentscope["agentscope"]
    ReAct[agent::ReActAgent]
    Toolkit[tool::Toolkit]
    Pipeline[pipeline::stream_printing_messages]
    Memory[memory/session]
    Model[model/formatter]
    ReAct --> Toolkit
    ReAct --> Memory
    ReAct --> Model
    Pipeline --> ReAct
  end

  subgraph 外部
    Provider[模型 API / DashScope/OpenAI/...]
    OTel[OpenTelemetry/观测平台]
  end

  UI --> AgentApp
  Runner --> ReAct
  ReAct --> Provider
  Tracing --> OTel
  ST_Server --> OTel
  ST_Server --> Runner
```

## 4. 模块调用关系图（跨项目）

```mermaid
flowchart LR
  subgraph runtime["agentscope-runtime"]
    A1[engine::AgentApp]
    A2[engine::Runner]
    A3[adapters::agentscope]
    A4[sandbox::SandboxManager]
    A1 --> A2
    A2 --> A3
    A2 --> A4
  end

  subgraph framework["agentscope"]
    B1[agent::ReActAgent]
    B2[tool::Toolkit]
    B3[pipeline::_functional]
    B4[model/formatter]
    B5[memory/session]
    B1 --> B2
    B1 --> B4
    B1 --> B5
    B3 --> B1
  end

  subgraph studio["agentscope-studio"]
    C1[server::index]
    C2[server::trpc/socket]
    C3[server::database]
    C1 --> C2
    C1 --> C3
  end

  A3 --> B3
  B2 -.->|可选| A4
  A2 -->|OTel| C1
```

## 5. 关键数据模型（抽象层）

- **消息（Msg/Block）**：Agent 输入输出统一为消息对象，工具调用使用 `ToolUseBlock/ToolResultBlock` 等 block 表达（见 `ReActAgent`/`AgentBase` 相关引用）。
- **工具（Tool Function / MCP / Skill）**：`Toolkit` 负责注册工具函数、MCP 客户端与 Skills，并以统一的“流式 ToolResponse”接口执行（`agentscope-codebase/agentscope/src/agentscope/tool/_toolkit.py`）。
- **会话与状态**：
  - 框架侧：Memory/Session 模块用于持久化对话与状态（在代码中以 module 方式组织）。
  - Runtime 侧：`AgentRequest` 携带 `session_id/user_id`，`Runner.stream_query` 会补全并以事件流形式输出（`agentscope-codebase/agentscope-runtime/src/agentscope_runtime/engine/runner.py`）。

## 6. 主要端到端流程（时序图）

下面用一个“典型服务化 + 可观测 + UI”的主流程描述跨组件协作：用户请求 → Runtime API → AgentScope ReAct → 模型/工具 → Sandbox → Trace → Studio UI。  
时序图参与者采用 **模块::参与者** 形式标注来源。

```mermaid
sequenceDiagram
  autonumber
  participant C as 外部::Client/UI
  participant RT as agentscope-runtime::engine::AgentApp
  participant R as agentscope-runtime::engine::Runner
  participant A as agentscope::agent::ReActAgent
  participant M as 外部::Model Provider API
  participant TK as agentscope::tool::Toolkit
  participant SB as agentscope-runtime::sandbox::SandboxManager
  participant TS as agentscope-runtime::engine::tracing
  participant ST as agentscope-studio::server
  participant UI as agentscope-studio::client

  C->>RT: POST /process (SSE) AgentRequest(input, session_id?)
  RT->>R: stream_query(request)
  R->>R: 补全 session_id/user_id, 初始化 AgentResponse 事件流
  R->>A: adapt_agentscope_message_stream(...)\n调用 agent(msgs)
  A->>M: Chat completion (stream)
  M-->>A: tokens/chunks
  A->>TK: 解析 ToolUseBlock 并执行工具（可能并行）
  alt 需要安全隔离执行
    TK->>SB: 调用 sandbox（HTTP/本地）执行工具
    SB-->>TK: 工具结果（stdout/files/etc）
  else 本地执行
    TK-->>A: 工具结果
  end
  A-->>R: 通过 stream_printing_messages/事件适配输出
  R-->>RT: yield Event/AgentResponse (SSE)
  RT-->>C: SSE streaming response

  par Trace 上报
    A-->>TS: trace_reply/trace_toolkit (OTel/Log)
    R-->>TS: trace(agent_step) (OTel/Log)
    TS-->>ST: /v1 traces (HTTP) 或 gRPC
    ST-->>UI: Socket.IO 推送 spans/runs/messages
  end
```

> 设计依据（代码入口）：  
> - `AgentApp` FastAPI 化与路由/协议注入：`agentscope-codebase/agentscope-runtime/src/agentscope_runtime/engine/app/agent_app.py`  
> - `Runner.stream_query` 的事件流与 session_id/user_id 补全：`agentscope-codebase/agentscope-runtime/src/agentscope_runtime/engine/runner.py`  
> - `ReActAgent` 以 Msg/Block 驱动 reasoning→act→observe：`agentscope-codebase/agentscope/src/agentscope/agent/_react_agent.py`  
> - `Toolkit` 的工具注册与执行（含 middleware/MCP/Skills）：`agentscope-codebase/agentscope/src/agentscope/tool/_toolkit.py`  
> - Studio server 的 OTEL/Socket/DB：`agentscope-codebase/agentscope-studio/packages/server/src/index.ts`、`.../database.ts`、`.../trpc/socket.ts`

## 7. 非功能性设计要点

- **可观测性**：框架与运行时均具备 tracing 能力（Runtime 侧显式提供 Log/Report/OTel 的组合，见 `agentscope-codebase/agentscope-runtime/src/agentscope_runtime/engine/tracing/README.md` 及中文补齐版本）。
- **安全性**：Runtime SandboxManager 支持本地/远端模式与容器隔离执行（Docker/K8s），并支持 Redis/本地映射维护 session/container 状态（`.../sandbox/manager/sandbox_manager.py`）。
- **可扩展性**：
  - 工具：Toolkit 支持函数 schema 自动解析、工具分组激活、MCP 客户端、Skills 目录化加载。
  - 协议：AgentApp 支持 A2A / Response API / AGUI 协议适配并注入 OpenAPI schema。

## 8. 架构图模块全覆盖清单（`agentscope_20260120.png`）

> 目标：确保图中**每个模块**都在设计文档中有对应说明或归属。
> 参考图文件：`agentscope-codebase/agentscope/assets/images/agentscope_20260120.png`

### 8.1 模型与服务提供方（左侧）

- Claude
- deepseek
- Gemini
- GLM
- OpenAI
- Qwen
- Azure
- Model Studio
- Ollama
- vLLM
- SGL
- NACOS

设计归属：上述提供方通过 AgentScope 的 `ChatModel/Multimodal/Realtime` 适配层接入，NACOS 在生态层用于服务发现/治理场景（按部署方案接入）。

### 8.2 数据与记忆底座（顶部中间）

- MySQL
- ORACLE
- PostgreSQL
- TableStore
- Qdrant
- mem0
- SQL Server
- OSS
- SQLite
- redis
- Milvus
- ReMe

设计归属：对应 AgentScope 的 Context & Memory（Memory Storage/RAG & Knowledge/Advanced Memory）与 Runtime 的状态/会话/追踪存储；向量库与记忆服务由 RAG/Memory 相关模块或外部服务接入。

### 8.3 AgentScope-Samples（开箱即用 Agents）

- Alias: General Assistant
- QA
- Browser-use
- Data-Juicer Agent
- Voice Agent
- Financial Analysis
- Data Science
- EvoTrader
- Deep Research
- More...

设计归属：均在 `agentscope-samples` 中体现，按“纯 Python / fullstack runtime”两种范式落地。

### 8.4 AgentScope（核心框架模块）

#### Model

- Chat Model
- Multi-modal Model
- Realtime Model

#### Tool

- Meta-Tool
- Function Call
- Agent Skills
- MCP Support
- Human-in-the-loop

#### Agent

- ReAct Agent
- Hooking Function
- A2A Agent

#### Context & Memory

- Memory Storage
- RAG & Knowledge
- Advanced Memory

#### Orchestration

- MsgHub
- Planning
- Pipeline

#### Tuner

- Workflow Function
- Task Dataset

#### Evaluation

- Evaluation Pipeline
- Graders

设计归属：以上均由 AgentScope 主仓中对应模块实现或示例覆盖（详见各子项目文档）。

### 8.5 AgentScope-Studio（图中模块）

- Tracing
- Evaluation Visualization
- Project Management
- Friday
- Chat UI

设计归属：Studio server/client + DB + Socket 架构中分别提供实时追踪、评测可视化、项目/运行管理与交互界面能力。

### 8.6 AgentScope-Runtime（图中模块）

- Tool Sandbox
- Deployment
- Agent-as-a-Service API
- Agent Serving

设计归属：Runtime 的 `SandboxManager + DeployManager + AgentApp/Runner` 对应实现服务化、部署与安全执行。

### 8.7 观测与评测生态（右侧）

- ARMS
- OpenTelemetry
- LoongSuite
- LangSmith
- Langfuse
- Phoenix
- SLS

设计归属：Runtime/Studio tracing 与外部观测平台对接，OTel 为核心标准接口。

### 8.8 周边生态与工具（右侧与底部）

- Data-juicer
- Trinity-RFT
- OpenJudge
- Spark Design

设计归属：分别对应数据处理、强化微调、评测框架与 UI 组件库生态位。

### 8.9 部署、协议与框架兼容（底部）

#### 部署环境

- ACK
- Kubernetes
- Docker
- FC
- Model Studio
- Knative

#### 协议/接口

- A2A
- A2UI
- AG-UI
- Response API

#### 多框架生态

- Agno
- crewai
- AutoGen
- LangGraph
- Microsoft Agent Framework
- More...

设计归属：由 Runtime 的部署层与协议适配层承接，并通过 adapter/协议路由实现跨框架兼容。

### 8.10 Sandbox 提供方生态（左下）

- AgentBay
- BoxLife
- E2B
- gVisor

设计归属：以上能力位于 Runtime 的 Tool Sandbox 生态层，作为安全执行底座候选，与 Docker/K8s/Serverless 运行环境组合使用。

