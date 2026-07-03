# アーキテクチャ概要

この文書は、現在の N.I.L.O. repository の実装境界を定義します。

## 目的

N.I.L.O. はローカル MCP server を提供します。主な layer は次の 3 つです。

- Core: 唯一の business logic layer。
- CLI: 人間向けの git-like local command interface。
- MCP Tool: Agent/LLM 向けの structured interface。

ユーザー向けのインストール、Notion connection 設定、コマンド利用方法は `Docs/JP/User/` にあります。この開発者 section は実装境界を記録します。

## 目標構造

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

必要な関係:

```text
CLI -> Core
MCP Tool -> Core
```

禁止:

```text
MCP tools invoking shell command strings
CLI -> Notion SDK
MCP Tool -> Notion SDK
```

## Core

Core は唯一の business logic layer です。責務は次の通りです。

- Global configuration の read/write、project context resolution、token redaction。
- Notion API version、timeout、retry の集中管理。
- Notion SDK-compatible client の作成。
- Auth validation と user/bot identity lookup。
- pages、blocks、databases、data sources、users、comments、views、file uploads、search、custom emojis の domain services。
- Raw API registry と controlled fallback calls。
- Local audit records と shared error model。

## CLI

CLI は人間向け entrypoint です。責務は次の通りです。

- Git-like command structure。
- Human-readable output。
- `--json` output。
- `--dry-run` preview。
- Local MCP server lifecycle commands。

公開 server commands:

```text
nilo server run
nilo server status
nilo server stop
nilo server logs
nilo server remove
nilo server stdio
```

CLI resource commands は Notion 操作のために Core services を呼び出します。

Project-local `.notion_mcp/` directory は project context と attachment state だけを保存します。token は保存しません。token、display name、Notion API version は global configuration に保存します。

## MCP Tool

MCP tools は Agent/LLM 向け entrypoint です。責務は次の通りです。

- Tool inventory。
- Input schemas。
- Tool annotations。
- Structured errors。
- Dangerous operations の confirmation requirements。

MCP tools は Core services を直接呼び出します。CLI command string は構築しません。

## 非機能境界

- Tokens は通常の CLI output や MCP configuration status に表示してはいけません。
- CLI/MCP の write operations は、必要に応じて dry-run preview または dangerous-operation confirmation を持つ必要があります。
- Live tests は default skip とし、明示的な test page/database/data source/workspace に対してのみ実行します。
- Notion-Version は Core configuration で管理し、CLI、MCP tools、個別 services に散在させません。
