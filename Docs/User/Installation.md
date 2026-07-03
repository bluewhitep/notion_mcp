# Installation

本文面向使用者，说明如何安装本地 Notion MCP 工具。

本文按场景分层：

- 安装：第一次让本机能运行 `nilo`。
- 更新或重新安装：先更新本地仓库，再重新安装当前包。
- 卸载：移除本地命令，或跳转到完整清理文档。

每个场景下再按安装方式分层：`uv` 持久安装、`uv` 临时运行、`pip` 安装。

## 使用前准备

推荐优先使用 `uv` 从本地路径安装。`uv tool install` 会把 `nilo` 命令安装到持久 tool 环境，并把可执行入口暴露到 PATH。

如果本机没有安装 `uv`，可以使用 `pip` 从本地路径安装。

安装完成后，需要先完成 Notion 侧 connection、token、page/database 授权和 id 查询。详细步骤见 [Configuration](Configuration.md) 的 “Notion 侧准备”。

安装后的第一组命令通常是：

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
```

新的配置命令统一使用 `nilo config --global ...`。

## 安装

### uv 持久安装

推荐第一次安装使用这种方式：

```bash
cd /path/to/notion-nilo
uv tool install .
nilo --help
```

如果安装后终端找不到 `nilo`，先确认 uv tool executable directory 已经在 PATH 中：

```bash
uv tool update-shell
```

然后重新打开终端再运行：

```bash
nilo --help
```

### uv 临时运行

不想持久安装时，可以从本地路径临时运行：

```bash
cd /path/to/notion-nilo
uv run --no-project --with . nilo --help
```

### pip 安装

没有 `uv` 时，可以用 `pip` 从本地路径安装：

```bash
pip install /path/to/notion-nilo
nilo --help
```

## 更新或重新安装当前包

如果当前仓库代码有更新，步骤是先更新本地仓库，再把本地 `nilo` 命令重新安装为当前包版本。如果 `git pull` 提示本地有未提交改动，先处理本地改动后再继续。

### uv 持久安装

```bash
cd /path/to/notion-nilo
git pull
uv tool install --force --reinstall .
nilo --help
```

### uv 临时运行

临时运行方式不需要重新安装持久命令。更新仓库后，下一次临时运行会使用当前本地路径：

```bash
cd /path/to/notion-nilo
git pull
uv run --no-project --with . nilo --help
```

### pip 安装

```bash
cd /path/to/notion-nilo
git pull
pip install --force-reinstall /path/to/notion-nilo
nilo --help
```

## 卸载

如果只需要移除命令行工具，按当初的安装方式执行对应命令。

### uv 持久安装

```bash
uv tool uninstall notion-nilo
```

### uv 临时运行

临时运行方式没有持久安装的 `nilo` 命令，不需要单独卸载。

### pip 安装

```bash
pip uninstall notion-nilo
```

### 完整清理

如果已经配置过 MCP client、后台 server、本地 token 或项目级 `.notion_mcp/` 上下文，请按 [Uninstallation](Uninstallation.md) 的完整清理顺序处理。
