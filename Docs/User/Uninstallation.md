# Uninstallation

本文面向使用者，说明如何卸载本地 `nilo`，以及哪些本地配置可以按需清理。

卸载本地工具不会删除 Notion 中的 page、database、block 或 comment。它也不会自动撤销 Notion Developer portal 里的 connection/token。如果不再使用该 connection，需要在 Notion 侧单独撤销或移除授权。

## 快速卸载

如果你只想移除命令行工具，按当初的安装方式执行对应命令。

### uv 持久安装

```bash
uv tool uninstall notion-nilo
```

### uv 临时运行

临时运行方式没有持久安装的 `nilo` 命令，不需要单独卸载。

如果仓库仍在本机，并且本机有 `uv`，仍可从本地路径临时运行：

```bash
uv run --no-project --with /path/to/notion-nilo nilo --help
```

### pip 安装

```bash
pip uninstall notion-nilo
```

## 完整清理

完整清理用于移除 MCP client 配置、后台 server runtime、本地 token 配置和项目级上下文。建议按下面顺序清理，尤其是已经配置过 MCP client 或后台 HTTP server 时。

### 停止并清理后台 server

如果曾经运行过 streamable-http 后台 server，先检查状态：

```bash
nilo server status
```

停止 server：

```bash
nilo server stop
```

清理 server runtime state 和日志：

```bash
nilo server remove
```

如果清理时需要强制停止 server，可以使用：

```bash
nilo server remove --force
```

默认 runtime 目录是当前全局配置文件所在目录。默认配置路径是 `~/.notion_mcp/config.json`，因此默认 server state 和日志通常也在 `~/.notion_mcp/` 下。若设置过 `NOTION_MCP_RUNTIME_DIR`，则以该环境变量指定的目录为准。

### 从 MCP client 中移除配置

如果 MCP client 使用 stdio 配置，删除对应的 `nilo` server 配置：

```json
{
  "mcpServers": {
    "nilo": {
      "command": "nilo",
      "args": ["server", "stdio"]
    }
  }
}
```

如果 MCP client 使用 streamable-http URL，删除对应的本地 URL 配置：

```text
http://127.0.0.1:8000/mcp
```

如果 client 中配置了 `NOTION_MCP_CONFIG` 环境变量，也一起删除。

### 卸载命令行工具

使用 `uv tool install .` 安装时：

```bash
uv tool uninstall notion-nilo
```

使用 `pip install /path/to/notion-nilo` 安装时：

```bash
pip uninstall notion-nilo
```

卸载后确认命令已经不可用：

```bash
nilo --help
```

如果终端仍然找到 `nilo`，说明它可能还通过其他 Python 环境、shell alias 或 PATH 中的其他位置安装过，需要检查当前 shell 的命令来源。

### 可选：删除全局配置

全局配置保存 Notion token、用户名、Notion API version、timeout、retry 等运行参数。默认路径是：

```text
~/.notion_mcp/config.json
```

确认不再需要本机 token 配置后再删除：

```bash
rm -f ~/.notion_mcp/config.json
```

如果你通过环境变量使用了其他配置路径，删除对应文件：

```bash
rm -f /path/to/config.json
```

### 可选：删除项目级上下文

项目级 `.notion_mcp/` 目录保存当前项目的本地上下文，例如默认 page/database 绑定、项目配置、state/cache/logs。它不保存全局 Notion token。

如果某个项目不再需要本地 Notion 上下文，可在该项目根目录执行：

```bash
rm -rf .notion_mcp
```

这只删除本地项目上下文，不会修改 Notion 远端内容。

### 可选：撤销 Notion 侧授权

如果你希望 token 彻底失效，或者不想让该 connection 继续访问已授权内容，需要到 Notion 侧撤销 internal connection/token，或从相关 page/database 的 connection 列表中移除该 connection。

本地卸载不会替你完成这一步。

## 清理后验证

### 验证本地命令

卸载持久命令后，运行下面命令应提示找不到 `nilo`，或显示当前 shell 中还有其他同名安装：

```bash
nilo --help
```

### 重新使用

如果全局配置也已经删除，重新安装后需要重新设置 token 才能调用 Notion API。配置步骤见 [Configuration](Configuration.md)。
