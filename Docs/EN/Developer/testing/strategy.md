# Testing Strategy

This document describes the test layers and execution strategy.

## Layers

- Compatibility tests
  - Keep public CLI and MCP tool behavior regression-testable.
  - Do not modify existing compatibility tests just to make a new implementation pass.
- Core tests
  - Cover configuration, errors, client factory, auth, services, Raw API, and audit.
- CLI tests
  - Cover init, config, status, resource commands, and dry-run behavior.
- MCP tests
  - Cover server lifecycle, tool inventory, tool calls, and dangerous tools.
- Scenario tests
  - Cover local configuration flows, CLI -> Core -> fake Notion, MCP -> Core -> fake Notion, and isolated install.
- Live tests
  - Skipped by default.
  - Access real Notion only when explicitly enabled with environment variables.

## Rules

- Write tests before implementing new behavior.
- Once tests exist, do not weaken them to pass a new implementation.
- Add narrower tests when coverage is insufficient.
- Never fake a passing live test.

## Common Commands

```bash
uv run pytest -q -p no:cacheprovider
uv run pytest -q tests/live
```

For isolated install checks:

```bash
uv run --no-project --with . nilo --help
uv run --no-project --with . nilo server run --help
```
