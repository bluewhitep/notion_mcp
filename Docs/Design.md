# 设计文档

本文档面向开发者，描述本地 Notion MCP 服务器的当前架构。legacy FastAPI REST 原型仍作为兼容层保留，但不是最终 MCP Tool 接口。

## 目标架构

当前架构是：

```text
Core + CLI + MCP Tool
```

调用边界：

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

设计原则：

- Core 负责唯一业务逻辑。
- CLI 负责人类可读、可调试、git-like 的本地体验。
- MCP Tool 负责 Agent/LLM 的结构化工具调用。
- CLI 不直接调用 Notion SDK。
- MCP Tool 不直接调用 Notion SDK。
- REST 原型路由只作为 legacy 兼容层，不能作为 MCP 的替代实现。

## 当前目录

```text
src/notion_mcp/
  core/
    config.py
    auth.py
    client.py
    errors.py
    models.py
    audit.py
    services/
      pages.py
      blocks.py
      databases.py
      data_sources.py
      users.py
      comments.py
      views.py
      file_uploads.py
      search.py
      custom_emojis.py
      raw_api.py
  cli/
    app.py
    commands/
  mcp_server/
    server.py
    tools/
  routes/
    legacy REST compatibility routes
```

## Core

Core 是唯一真实能力来源，负责：

- 配置初始化、读取、更新、权限控制和 token 脱敏。
- Notion client 初始化，集中注入 token、Notion API version、timeout、retry。
- auth 校验和 bot/self/user 信息读取。
- Notion 对象域服务：
  - pages
  - blocks
  - databases
  - data sources
  - users
  - comments
  - views
  - file uploads
  - search
  - custom emojis
- 受控 raw/pass-through 操作入口。
- 本地审计记录，包含 configured user UUID、操作类型、目标对象、dry-run 状态和时间。
- 统一错误模型，供 CLI 和 MCP Tool 共同使用。

Core 不导入 CLI、MCP server 或 legacy REST routes。

## CLI

CLI 只做终端用户体验：

- `notion-mcp init`
- `notion-mcp config --global --show`
- `notion-mcp config --local --show`
- `notion-mcp auth validate`
- `notion-mcp page ...`
- `notion-mcp database ...`
- `notion-mcp mcp serve`

CLI 输出分两类：

- 普通文本：给人读。
- `--json`：给程序和 Agent 调试用。

写操作必须支持 `--dry-run`，并通过 Core 执行 dry-run 分支。

## MCP Tool

MCP Tool 是 Agent/LLM 的正式结构化入口。它必须：

- 使用 MCP Python SDK 创建真正 MCP server。
- 支持 tools 枚举和 tool 调用。
- 为每个 tool 提供名称、说明、输入 schema、输出结构和危险操作说明。
- 直接调用 Core。
- 把 Core 错误转换为 MCP tool 结果。

初始工具域：

- config
- auth
- pages
- blocks
- databases
- data_sources
- users
- comments
- views
- file_uploads
- search
- custom_emojis
- raw_api

## Legacy REST

当前 FastAPI REST 路由保留为 legacy compatibility：

- 它们用于证明迁移过程中旧行为没有被破坏。
- 它们不是 MCP Tool，也不能作为 Agent/LLM 的最终正式工具接口。

## 配置模型

配置字段：

- `notion_token`
- `user_name`
- `user_id`
- `notion_version`
- `default_transport`
- `config_path`

安全要求：

- token 存储文件权限应限制为当前用户读写。
- `show`、`status` 和 MCP `config_status` 默认脱敏 token。
- live 测试不得输出真实 token。

## API version 策略

Core 集中管理 Notion API version。

默认目标版本是 `2026-03-11`。所有服务必须通过 Core client 工厂使用统一版本，不允许在 CLI、MCP tool 或单个服务里散落硬编码版本。

## 测试策略

- legacy 测试：保持不修改，用于保护旧 FastAPI REST 和旧 CLI 行为。
- Core 测试：验证 Core 业务逻辑、配置、client factory、service 和错误模型。
- CLI 测试：验证 CLI 到 Core 的调用边界、human output、JSON output 和 dry-run。
- MCP 测试：验证 MCP server 生命周期、tool inventory、tool call 和危险操作确认。
- 场景测试：验证隔离安装、端到端 mock workflow 和项目上下文解析。
- live 测试：访问真实 Notion 环境，默认跳过。
