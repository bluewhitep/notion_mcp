# Live 测试文档

本文档面向开发者，记录真实 Notion 环境测试的门控方式和安全要求。

## 默认行为

live 测试默认跳过，不会在普通测试命令中访问 Notion。

当前 live 测试：

- `tests/live/test_live_auth_validate.py`
  - 默认跳过原因：需要真实 token。
  - 启用条件：`NOTION_MCP_LIVE=1` 和 `NOTION_MCP_TOKEN`。
  - 可选条件：`NOTION_MCP_USER_ID`，用于校验 token 对应用户。

## 启用方式

```bash
NOTION_MCP_LIVE=1 \
NOTION_MCP_TOKEN=ntn_xxx \
NOTION_MCP_USER_ID=01234567-89ab-cdef-0123-456789abcdef \
uv run pytest -q tests/live
```

## 安全要求

- live 测试不得修改生产数据。
- 如未来加入写操作 live 测试，只能使用测试 workspace 或测试页面。
- 缺少 token、权限、付费计划或测试 workspace 时必须跳过，不能伪造通过。
