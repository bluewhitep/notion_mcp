# notion-mcp

This repository provides a local Notion MCP server with a Core + CLI + MCP Tool architecture.

## Status

- Core is the only business logic layer.
- CLI is the git-like human entrypoint.
- MCP tools are the structured Agent/LLM entrypoint.
- Background MCP server lifecycle commands are available through `notion-mcp server ...`.

The project is in alpha. Public APIs, CLI commands, and MCP tool contracts may still change before a stable release.

## Installation

### PyPI release

Use this method after the first PyPI release is published:

```bash
uv tool install notion-mcp
notion-mcp --help
```

If you do not use `uv`, install with `pip` instead:

```bash
pip install notion-mcp
notion-mcp --help
```

### GitHub source

Use this method to install directly from the public source repository:

```bash
git clone https://github.com/bluewhitep/notion_mcp.git
cd notion_mcp
uv tool install .
notion-mcp --help
```

## Documentation

- [Installation](Docs/User/Installation.md)
- [Configuration](Docs/User/Configuration.md)
- [MCP client setup](Docs/User/MCP_Clients.md)
- [CLI reference](Docs/User/Cli.md)
- [Troubleshooting](Docs/User/Troubleshooting.md)
- [Developer packaging notes](Docs/Developer/packaging.md)

## Roadmap

- Publish the initial PyPI package from GitHub Release `v0.2.0`.
- Keep GitHub source installation available for users who want the latest repository state before a PyPI release.

## Development

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
```

Live Notion tests require explicit opt-in and real Notion credentials. Do not commit tokens or local configuration files.

## Security

Report non-sensitive bugs through [GitHub issues](https://github.com/bluewhitep/notion_mcp/issues). For sensitive security reports, follow [SECURITY.md](SECURITY.md).

## Contributing

Pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

## License

Licensed under the [Apache License 2.0](LICENSE).
