# Project Config CLI

本文说明项目上下文和配置相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp init` | 在当前目录创建项目级 `.notion_mcp/`，用于记录当前目录的 Notion 上下文。 |
| `notion-mcp pwd` | 从当前目录向上查找项目配置，并输出解析到的项目根目录。 |
| `notion-mcp version` | 显示 Notion MCP 版本和当前配置的 Notion API version。 |
| `notion-mcp config --global --show` | 查看全局配置状态：是否已配置、token 是否已设置、用户名称和 Notion API version。 |
| `notion-mcp config --global user.token <token>` | 设置当前用户级 Notion token。 |
| `notion-mcp config --global user.name <name>` | 设置当前用户级显示名称。 |
| `notion-mcp config --local --show` | 查看当前仓库或目录树的项目级配置。 |

## 示例

```bash
notion-mcp init --project-name "Demo"
notion-mcp pwd
notion-mcp version --json
notion-mcp config --global user.token ntn_xxx
notion-mcp config --global user.name "Ada"
notion-mcp config --global --show
notion-mcp config --local --show --json
```

全局配置保存 token 和运行参数；项目级配置不保存 token。普通用户不需要手动填写 `user_id`，需要查看当前 token 身份时使用 `notion-mcp auth whoami --json`。
