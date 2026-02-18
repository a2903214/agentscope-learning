# AgentScope Studio 总体设计

> 代码根目录：`s:\agentscope\agentscope-codebase\agentscope-studio`  
> 主要模块：`packages/server`（服务端）、`packages/client`（前端）

## 1. 定位与目标

Studio 是面向开发者的本地可视化工具，用于：

- 项目（Projects）与运行（Runs）管理
- Chatbot 风格交互展示（运行时消息流）
- Tracing 可视化（OTel spans、模型调用统计）
- 评测与分析（Evaluation）

## 2. 架构概览

Studio 由 **server + client** 构成：

- **Server（Node/Express）**
  - TRPC API：`/trpc`
  - OTEL HTTP 接收：`/v1`（支持 protobuf/octet-stream/json）
  - OTEL gRPC 接收：独立端口启动 gRPC server（失败则退化到仅 HTTP）
  - Socket.IO：向 client 推送 projects/runs/messages/spans 的实时更新
  - DB：TypeORM 管理数据表、视图与迁移
- **Client（Vite/React）**
  - 订阅 Socket.IO 事件获取实时数据
  - 通过 TRPC 拉取/管理项目与运行
  - 展示 traces、token、模型调用等统计

## 3. 关键入口与模块

### 3.1 Server 启动入口

**实现位置**：`agentscope-codebase/agentscope-studio/packages/server/src/index.ts`

启动关键步骤（从代码可见）：

- 读取配置（`ConfigManager`），探测可用 HTTP 端口与 OTEL gRPC 端口（`portfinder`）。
- 初始化 Express + HTTP server。
- 初始化数据库（`initializeDatabase`）。
- 注册路由：
  - `/trpc`：TRPC middleware（`appRouter`）
  - `/v1`：OTEL HTTP（raw body + `otelRouter`）
- 初始化 Socket.IO（`SocketManager.init(httpServer)`）。
- 启动 OTEL gRPC server（`OtelGrpcServer.start(port)`），失败则提示并退化。
- 生产模式下提供静态资源并自动打开浏览器。

### 3.2 数据库层

**实现位置**：`agentscope-codebase/agentscope-studio/packages/server/src/database.ts`

- `initializeDatabase` 以 TypeORM `DataSource` 初始化数据库，加载 entities（Run/Message/Reply/InputRequest/Span 等）并自动运行 migrations。
- 启动时会执行一次“数据刷新”：更新 run 状态与 input request。

### 3.3 Socket 实时推送

**实现位置**：`agentscope-codebase/agentscope-studio/packages/server/src/trpc/socket.ts`

Socket namespaces（从代码可见）：

- `/friday`：Friday app client（可中断 reply）
- `/python`：Python client（run_id 绑定；断连时清理 input requests 并更新 run 状态）
- `/client`：Studio 前端 client（加入 project/run/overview 等房间，接收 runs/messages/spans 推送）

## 4. 代码结构分析

代码根路径：`agentscope-codebase/agentscope-studio/packages/`。

| 包/目录 | 职责 | 代表路径 |
|---------|------|----------|
| `server/` | Express 服务、TRPC、OTEL、Socket、DB | `src/index.ts`、`src/trpc/`、`src/otel/`、`src/database.ts` |
| `server/src/index.ts` | 启动入口、端口探测、路由注册、Socket/OTEL gRPC 启动 | `index.ts` |
| `server/src/database.ts` | TypeORM 初始化、entities、migrations | `database.ts` |
| `server/src/trpc/` | TRPC router、SocketManager、房间与推送逻辑 | `socket.ts`、router 等 |
| `server/src/otel/` | OTEL HTTP/gRPC 接收、proto 与处理 | `otelRouter`、`OtelGrpcServer` 等 |
| `client/` | Vite/React 前端、页面与 Socket 订阅 | `packages/client` 下 src |

## 5. 技术架构框图

```mermaid
flowchart TB
  subgraph client["packages/client"]
    UI[React 应用]
    TRPC_C[TRPC 客户端]
    Socket_C[Socket.IO 客户端]
    UI --> TRPC_C
    UI --> Socket_C
  end

  subgraph server["packages/server"]
    Express[Express]
    TRPC[TRPC middleware /trpc]
    OTEL_HTTP[OTEL HTTP /v1]
    OTEL_GRPC[OTEL gRPC]
    Socket[SocketManager /client /python /friday]
    DB[(TypeORM DB)]
    Express --> TRPC
    Express --> OTEL_HTTP
    Express --> Socket
    TRPC --> DB
    OTEL_HTTP --> DB
    Socket --> DB
  end

  TRPC_C --> TRPC
  Socket_C --> Socket
```

## 6. 模块调用关系图

```mermaid
flowchart LR
  subgraph server["server"]
    Index[index.ts]
    DB[database.ts]
    Socket[trpc/socket.ts]
    Otel[otel]
    Index --> DB
    Index --> Socket
    Index --> Otel
    Socket --> DB
    Otel --> DB
  end
  subgraph client["client"]
    App[React App]
  end
  App --> Socket
  App --> Index
```

## 7. 主要流程时序图（Client 进入某个 Run）

参与者采用 **模块::参与者** 形式标注来源。

```mermaid
sequenceDiagram
  autonumber
  participant UI as agentscope-studio::client
  participant IO as agentscope-studio::server::trpc::Socket.IO
  participant DAO as agentscope-studio::server::RunDao/InputRequestDao/SpanDao
  participant DB as agentscope-studio::server::database::TypeORM

  UI->>IO: connect + joinProjectRoom(project)
  IO->>DAO: doesProjectExist + getAllProjectRuns
  DAO->>DB: query runs/projects
  DB-->>DAO: result
  DAO-->>IO: runs data
  IO-->>UI: pushRunsData

  UI->>IO: joinRunRoom(runId)
  IO->>DAO: doesRunExist + getRunData(runId)
  DAO->>DB: query run/messages/replies/spans
  DB-->>DAO: result
  IO-->>UI: pushRunData/pushInputRequests/pushMessages/pushSpans
```

