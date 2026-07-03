# Installation

This document explains how to install, update, and uninstall the local `nilo` command.

## Before You Start

The recommended flow uses `uv tool install`, which installs the `nilo` command into a persistent tool environment and exposes it on your shell `PATH`.

If `uv` is not available, use `pip` from the local repository path.

After installation, configure your Notion internal connection token before making API calls. See [Configuration](Configuration.md).

The first commands are usually:

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
```

## Installation

### Persistent uv Install

Use this for the normal local installation:

```bash
cd /path/to/notion-nilo
uv tool install .
nilo --help
```

If the shell cannot find `nilo`, update the uv shell integration and restart the terminal:

```bash
uv tool update-shell
nilo --help
```

### Temporary uv Run

Use this when you do not want to install a persistent command:

```bash
cd /path/to/notion-nilo
uv run --no-project --with . nilo --help
```

### pip Install

Use this when `uv` is not available:

```bash
pip install /path/to/notion-nilo
nilo --help
```

## Update

When the repository changes, update the local checkout first, then reinstall the command. If `git pull` reports local changes, resolve those changes before reinstalling.

### Persistent uv Install

```bash
cd /path/to/notion-nilo
git pull
uv tool install --force --reinstall .
nilo --help
```

### Temporary uv Run

Temporary execution always uses the current local path:

```bash
cd /path/to/notion-nilo
git pull
uv run --no-project --with . nilo --help
```

### pip Install

```bash
cd /path/to/notion-nilo
git pull
pip install --force-reinstall /path/to/notion-nilo
nilo --help
```

## Uninstall

### Persistent uv Install

```bash
uv tool uninstall notion-nilo
```

### Temporary uv Run

No uninstall step is needed because no persistent `nilo` command was installed.

### pip Install

```bash
pip uninstall notion-nilo
```

### Full Cleanup

If you also configured an MCP client, background server runtime, global token, or project-local `.notion_mcp/` context, follow the full cleanup order in [Uninstallation](Uninstallation.md).
