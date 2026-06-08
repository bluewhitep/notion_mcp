# Architecture Overview

本文档面向开发者，说明当前仓库的架构边界。

## 目标结构

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
Legacy REST -> Core-compatible adapter or legacy compatibility layer
```

必须保持：

```text
CLI -> Core
MCP Tool -> Core
```

禁止：

```text
MCP Tool 通过 CLI 字符串绕行
CLI -> Notion SDK
MCP Tool -> Notion SDK
```

## Core

Core 是唯一业务逻辑层，负责：

- 配置读写和 token 脱敏。
- Notion API version 管理。
- Notion SDK client 创建。
- auth validate。
- 按对象域封装 Notion 服务。
- raw API 登记表。
- 本地审计。

## CLI

CLI 是人类入口，负责：

- git-like 命令结构。
- 普通文本输出。
- `--json` 输出。
- `--dry-run`。
- 启动 MCP server。

CLI resource command 通过 Core service 调用 Notion 能力。

## MCP Tool

MCP Tool 是 Agent/LLM 入口，负责：

- tool inventory。
- input schema。
- tool annotations。
- 结构化错误。
- 危险操作确认。

MCP Tool 直接调用 Core service，不拼 CLI 字符串。

## Legacy REST

legacy FastAPI REST 路由仍保留，用于旧测试和旧入口兼容。它不是最终 MCP 接口。
