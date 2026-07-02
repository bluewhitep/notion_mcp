# Contributing

Pull requests are welcome.

## Before Opening a Pull Request

Use a small, focused change. Keep unrelated refactors, formatting churn, and
generated files out of the PR.

Run the local checks when they apply:

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
```

Live Notion tests require explicit opt-in and real credentials. Do not run or
document live results unless the test command, required environment variables,
and data-safety scope are clear.

## Documentation

Update user or developer documentation when a change affects CLI commands,
MCP tools, configuration, installation, security behavior, or public package
metadata.

## Security

Do not include real Notion tokens, private workspace content, local config files,
or unredacted logs in issues, pull requests, tests, or documentation.

Report sensitive security issues through the process in [SECURITY.md](SECURITY.md).

## License

By contributing to this repository, you agree that your contribution is licensed
under the Apache License 2.0.
