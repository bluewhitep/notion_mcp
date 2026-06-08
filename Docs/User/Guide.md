# 使用指南

本文面向最终使用者，介绍如何安装并使用本地 Notion MCP 服务。通过本服务，可以在 AI 工具或脚本中调用 Notion API，实现页面、数据库、区块等对象域的读取和写入。

## 当前状态

当前可用入口包括 git-like CLI、本地 MCP server 和 legacy FastAPI REST 兼容入口。

CLI 使用说明见 `Docs/User/cli.md`。
MCP client 使用说明见 `Docs/User/mcp_clients.md`。

## 前提条件

1. **创建 Notion 集成**：在使用本服务前，需要先在 Notion 中创建内部集成，并记录生成的集成 token。
2. **授予页面访问权限**：在 Notion 中将需要访问的页面或数据库连接到该集成。
3. **安装 Python 3.10+**：本项目基于 Python 开发，请确保系统已安装 Python 3.10 或更高版本。

## 安装

推荐使用 uv 隔离运行：

```bash
uv run --with /path/to/notion_mcp_project notion-mcp --help
```

更完整的安装说明见 `Docs/User/installation.md`。

## 初始化配置

首次使用需设置 Notion 集成 token 和当前用户 UUID。

```bash
# 运行初始化命令，按照提示输入 token、用户名和用户 UUID
notion-mcp init

# 或直接通过参数指定，跳过交互
notion-mcp init --token ntn_xxx --user-name Ada --user-id 01234567-89ab-cdef-0123-456789abcdef

# 查看保存的配置
notion-mcp status --json

# 更新 token 或用户 ID
notion-mcp config set notion_token 新的token
notion-mcp config set user_id 新的用户UUID
```

配置文件默认存储在 `~/.notion_mcp/config.json`。可以通过环境变量 `NOTION_MCP_CONFIG` 指定其他路径。

## 启动 MCP Server

运行以下命令启动本地 MCP server：

```bash
notion-mcp mcp serve --transport stdio
```

MCP client 配置说明见 `Docs/User/mcp_clients.md`。

## 调用示例

CLI 示例：

```bash
notion-mcp page retrieve <page_id> --json
notion-mcp database query <database_id> --json
notion-mcp block children <block_id> --json
```

## 常见问题

### 1. 为什么提示“未设置 Notion token”？

这是因为在调用接口前未运行 `notion-mcp init` 或未设置 token。请按照初始化步骤设置 token。

### 2. 如何找到我的 Notion 用户 UUID？

你可以访问 `https://api.notion.com/v1/users/me` 并在响应中查找 `id` 字段，也可以通过 Notion 后台的个人信息界面获取。该 UUID 用于标识编辑者。

### 3. 是否支持 OAuth 授权？

当前版本仅支持内部集成 token。如需 OAuth 支持，可以在项目开发计划中提出需求；未来版本可能会支持。

### 4. 调用返回错误怎么办？

一般情况下，错误来自配置、权限或 Notion API 参数。请检查：

1. 是否已正确设置 token 且没有过期；
2. 是否已授权集成访问对应的页面或数据库；
3. 调用参数是否符合 Notion API 要求。

若确认上述问题均无误，可查看 CLI 输出、MCP client 日志或本地服务日志。

---

本指南介绍了从安装到使用本地 Notion MCP 服务的完整流程。更多开发者接口说明请参阅 `Docs/Developer/API.md`。
