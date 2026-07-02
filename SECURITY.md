# Security Policy

## Reporting a Vulnerability

Report non-sensitive bugs and support issues through GitHub issues:

https://github.com/bluewhitep/notion_mcp/issues

Do not open a public issue for secrets, token exposure, privilege escalation,
remote execution, authentication bypass, or other sensitive security reports.
For sensitive reports, use GitHub private vulnerability reporting:

https://github.com/bluewhitep/notion_mcp/security/advisories/new

If private vulnerability reporting is not enabled or unavailable, open a public
issue requesting a private maintainer contact channel, but do not include
vulnerability details, tokens, workspace data, or exploit steps in that public
issue.

Please include:

- A short description of the vulnerability.
- Reproduction steps or a minimal proof of concept.
- The affected version, commit, command, or MCP tool.
- Whether real Notion tokens, workspace data, or user data were exposed.

## Scope

Security reports are in scope when they affect this repository's local CLI,
Core layer, MCP server, MCP tools, packaging, or documented configuration.

The following are usually out of scope:

- Issues caused only by a compromised local machine.
- Reports that require a real Notion workspace without a clear project defect.
- Denial-of-service reports without a realistic impact path.

## Token Handling

Do not include real Notion tokens, private workspace data, or local config files
in public issues, pull requests, logs, screenshots, or test fixtures.
