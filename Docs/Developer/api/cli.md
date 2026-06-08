# CLI API

本文档面向开发者，记录当前 `src/notion_mcp/cli/` 的人类入口设计。CLI 负责终端使用体验，业务能力来自 `src/notion_mcp/core/`。

## 入口

- package：`notion_mcp.cli`
- console script：`notion-mcp = notion_mcp.cli:app`
- root app：`src/notion_mcp/cli/app.py`

## 命令结构

- `notion-mcp init`
  - 写入 Core 配置。
  - 支持 `--token`、`--user-name`、`--user-id`、`--notion-version`、`--json`。
  - `--user` 是 legacy alias，仅用于保留旧入口兼容。
- `notion-mcp status`
  - 输出配置和能力状态。
  - `--json` 返回稳定结构。
- `notion-mcp config get/set/unset/list`
  - git-like 配置命令。
  - token 默认脱敏，除非显式使用 `--show-secret`。
- `notion-mcp auth validate`
  - 通过 Core auth service 校验 token。
- `notion-mcp page ...`
  - 支持 `retrieve`、`create`、`update`、`trash`。
  - `create`、`update`、`trash` 支持 `--dry-run`。
- `notion-mcp block ...`
  - 支持 `children`、`append`。
  - `append` 支持 `--dry-run`。
- `notion-mcp database ...`
  - 支持 `retrieve`、`query`。
  - `query` 支持 `--dry-run`。
- `notion-mcp data-source ...`
  - 支持 `retrieve`、`query`、`create`、`update`。
  - 写操作支持 `--dry-run`。
- `notion-mcp user ...`
  - 支持 `me`、`list`、`retrieve`。
- `notion-mcp comment ...`
  - 支持 `list`、`create`、`reply`。
  - 写操作支持 `--dry-run`。
- `notion-mcp view ...`
  - 支持 `retrieve`、`list`、`query`、`create`、`update`。
  - 写操作支持 `--dry-run`。
- `notion-mcp file-upload ...`
  - 支持 `retrieve`、`list`、`create`、`send`、`complete`。
  - 写操作支持 `--dry-run`。
- `notion-mcp search query`
  - 通过 Core search service 查询 workspace。
- `notion-mcp custom-emoji ...`
  - 支持 `list`、`retrieve`。
- `notion-mcp raw-api ...`
  - 支持 `operations` 和受控 `invoke`。
- `notion-mcp mcp serve`
  - 启动本地 MCP server。
  - 支持 `--transport stdio` 和 `--transport streamable-http`。

## 兼容命令

以下 legacy 命令保留，用于现有测试和旧用户迁移：

- `notion-mcp set-token`
- `notion-mcp set-user`
- `notion-mcp show`
- `notion-mcp run`

其中 `run` 启动 legacy FastAPI REST 服务，不是 MCP server。

## 调用边界

CLI resource command 不直接导入 Notion SDK。当前实现通过 `src/notion_mcp/cli/core_services.py` 创建 Core service，再由 Core service 调用 SDK-compatible client。

正确关系：

```text
Human -> CLI -> Core -> Notion SDK
```

禁止关系：

```text
CLI -> Notion SDK
MCP Tool -> CLI 字符串
```
