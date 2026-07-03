# Skills Template Library

## Purpose
This directory stores reusable skill templates for Codex, Claude, and other agent or tool ecosystems.

The templates use shared reference manuals so the same operating rules can be reused without copying long instructions into every tool-specific skill file.

For Codex runtime discovery, repository-level skills live under `.agents/skills/`. `Docs/EN/Developer/Reference/Skills/` is the template and documentation library used to design or copy those runtime skills.

## Layout
```text
Docs/EN/Developer/Reference/Skills/
  README.md
  CHANGELOG.md
  references/
    quick.md
    normal.md
    full.md
  codex/
    SKILL.md
  claude/
    SKILL.md
  third_party/
    SKILL.md
  test_copies/
    README.md
    codex/
      SKILL.md
    references/
      quick.md
      normal.md
      full.md
```

## Reference Levels
- `references/quick.md`: fast usage guide. Use it to decide which scenario applies and what to do next.
- `references/normal.md`: standard usage guide. Use it for common multi-step work, more detailed routing, and light troubleshooting.
- `references/full.md`: complete usage guide. Use it for edge cases, template adaptation, and deeper troubleshooting.

## Template Policy
- Keep shared behavior in `references/`.
- Keep tool-specific files small and focused on routing.
- Do not duplicate the full reference manuals inside each `SKILL.md`.
- Add a new tool-specific directory only when that tool needs different entrypoint format, metadata, or invocation guidance.
- Use `test_copies/` only for local repository testing. Do not treat it as the canonical template source.
- When one workflow has both server and CLI surfaces, keep server and CLI guidance separated inside the references. Split into separate top-level skills only if trigger scope or validation diverges enough to make one wrapper ambiguous.
