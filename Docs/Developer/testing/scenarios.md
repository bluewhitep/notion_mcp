# 场景测试文档

本文档面向开发者，说明离线场景测试和 fake Notion client 的使用方式。详细历史记录保存在开发进度资料中。

## Fake Notion Client

Fake Notion client 用于离线验证 CLI/MCP/Core 调用链，不访问真实 Notion workspace。

主要用途：

- 模拟 `users.me()`。
- 模拟 page retrieve/create/update、block children/append/update/trash、database/data source 查询等对象域能力。
- 记录调用序列，验证 CLI 和 MCP Tool 是否通过 Core service 到达 fake client。
- 验证 dry-run 不调用真实写入分支。

## 场景覆盖

- 全局配置流程：设置 token、查看 status、验证 auth。
- CLI 到 Core 到 fake Notion：验证人类 CLI 命令走 Core service。
- MCP 到 Core 到 fake Notion：验证 MCP tool 调用走 Core service。
- 安装和 help：验证隔离安装后的 root help、resource help 和 MCP serve help。
- 项目上下文：验证项目级 `.notion_mcp/` 初始化、从子目录发现项目 root、page/database attach 后省略 id。
- Page 内容编辑：验证 page content、insert-after、append、update、remove 的页面内容编辑闭环。
- Database/DataSource：验证 database attach、active data source defaulting、query、page create/update 和 property rename。
- Live 内容一致性：在显式 opt-in 后，对真实 Notion page、block 和 data source entry 执行 create/read/compare/update/read/compare/trash/verify。

## 常用验证命令

场景测试可和全量测试一起运行：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_scenarios uv run pytest -q -p no:cacheprovider
```

## 备注

- 场景测试默认使用 fake client，不需要真实 token。
- 真实 Notion workspace 场景必须使用 live/integration 标记，并默认跳过。
- 严格内容一致性 live E2E 位于 `tests/live/test_live_content_consistency_e2e.py`。运行前必须确认目标是专用测试 page/data source，并显式开启：

```bash
env \
  PYTHONDONTWRITEBYTECODE=1 \
  UV_CACHE_DIR=/private/tmp/notion_mcp_uv_live_e2e \
  NOTION_MCP_LIVE_E2E=1 \
  NOTION_MCP_LIVE_PARENT_PAGE_ID=<test_page_id> \
  NOTION_MCP_LIVE_DATA_SOURCE_ID=<test_data_source_id> \
  uv run pytest -q -p no:cacheprovider tests/live/test_live_content_consistency_e2e.py
```
