# N.I.L.O.

N.I.L.O. - Notion Interfaces, Locally Operated - provides a local Notion runtime with a Core + CLI + MCP Tool architecture.

## Status

- Core is the only business logic layer.
- CLI is the git-like human entrypoint.
- MCP tools are the structured Agent/LLM entrypoint.
- Background MCP server lifecycle commands are available through `nilo server ...`.

The project is in alpha. Public APIs, CLI commands, and MCP tool contracts may still change before a stable release.

## Installation

### PyPI release

Use this method after the first PyPI release is published:

```bash
uv tool install notion-nilo
nilo --help
```

If you do not use `uv`, install with `pip` instead:

```bash
pip install notion-nilo
nilo --help
```

### GitHub source

Use this method to install directly from the public source repository:

```bash
git clone https://github.com/bluewhitep/notion-nilo.git
cd notion-nilo
uv tool install .
nilo --help
```

## Migration From notion-mcp

The previously published `notion-mcp` PyPI project remains separate and will not be renamed by PyPI. New releases use:

- PyPI package: `notion-nilo`
- Python import package: `nilo`
- CLI command: `nilo`
- GitHub repository: `bluewhitep/notion-nilo`

Existing `.notion_mcp/` project context directories and `NOTION_MCP_*` environment variables are intentionally kept for compatibility in this rename.

## Documentation

- [Installation](Docs/User/Installation.md)
- [Configuration](Docs/User/Configuration.md)
- [MCP client setup](Docs/User/MCP_Clients.md)
- [CLI reference](Docs/User/Cli.md)
- [Troubleshooting](Docs/User/Troubleshooting.md)
- [Developer packaging notes](Docs/Developer/packaging.md)

## Roadmap

- Publish the first `notion-nilo` PyPI release from GitHub Release `v_0.3.0`.
- Consider a final `notion-mcp` migration notice release that points users to `notion-nilo`.
- Keep GitHub source installation available for users who want the latest repository state before a PyPI release.

## Development

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
```

Live Notion tests require explicit opt-in and real Notion credentials. Do not commit tokens or local configuration files.

## Security

Report non-sensitive bugs through [GitHub issues](https://github.com/bluewhitep/notion-nilo/issues). For sensitive security reports, follow [SECURITY.md](SECURITY.md).

## Contributing

Pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

## License

Licensed under the [Apache License 2.0](LICENSE).
