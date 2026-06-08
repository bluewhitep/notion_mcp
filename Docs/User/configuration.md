# Configuration

本文面向使用者，说明如何配置 Notion token、用户名和用户 UUID。

## 初始化配置

```bash
notion-mcp init \
  --token ntn_xxx \
  --user-name "Ada" \
  --user-id 01234567-89ab-cdef-0123-456789abcdef
```

## 查看状态

```bash
notion-mcp status
notion-mcp status --json
```

token 在普通状态输出和 JSON 状态输出中都会脱敏。

## 修改配置

```bash
notion-mcp config set user_name "Ada Lovelace"
notion-mcp config get user_name
notion-mcp config list
```

## 配置路径

默认配置文件位于当前用户目录下的 `.notion_mcp/config.json`。

可以通过环境变量指定其他路径：

```bash
NOTION_MCP_CONFIG=/path/to/config.json notion-mcp status
```

## Notion API Version

默认 Notion API version 为 `2026-03-11`。

如需覆盖：

```bash
notion-mcp config set notion_version 2026-03-11
```
