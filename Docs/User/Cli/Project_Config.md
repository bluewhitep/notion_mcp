# Project Config CLI

本文说明项目上下文和配置相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo init` | 在当前目录创建项目级 `.notion_mcp/`，用于记录当前目录的 Notion 上下文。 |
| `nilo pwd` | 从当前目录向上查找项目配置，并输出解析到的项目根目录。 |
| `nilo version` | 显示 Notion MCP 版本和当前配置的 Notion API version。 |
| `nilo config --global --show` | 查看全局配置状态：是否已配置、token 是否已设置、用户名称和 Notion API version。 |
| `nilo config --global user.token <token>` | 设置当前用户级 Notion token。 |
| `nilo config --global user.name <name>` | 设置当前用户级显示名称。 |
| `nilo config --local --show` | 查看当前仓库或目录树的项目级配置。 |

## 示例

```bash
nilo init --project-name "Demo"
nilo pwd
nilo version --json
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo config --local --show --json
```

全局配置保存 token 和运行参数；项目级配置不保存 token。普通用户不需要手动填写 `user_id`，需要查看当前 token 身份时使用 `nilo auth whoami --json`。
