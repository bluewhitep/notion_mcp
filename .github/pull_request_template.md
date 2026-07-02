## Summary

- 

## Validation

- [ ] `uv run pytest -q -p no:cacheprovider`
- [ ] `uv run ruff check .`
- [ ] `uv run mypy src`
- [ ] Documentation updated, or not applicable

## Safety

- [ ] No real Notion tokens, private workspace data, local config files, or unredacted logs are included.
- [ ] Live Notion tests were not run, or their credential/data scope is documented.
