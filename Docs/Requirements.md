# 需求说明

本文档面向开发者，描述本地 Notion MCP 服务器的目标需求、历史 legacy prototype 范围和当前实现状态。使用者安装与调用说明放在 `Docs/User/`，不在本文档展开。

## 背景

Notion 官方提供远程托管的 Notion MCP 服务，面向常见 AI 工具使用 OAuth 授权。当前仓库选择补全一个本地自托管 MCP 服务器，服务于需要 bearer token、内部集成 token、personal access token、自动化执行或复用已有 Notion connection 的场景。

Notion API 是 versioned API，Core 层必须集中管理 `Notion-Version`。当前开发目标以 `2026-03-11` 为默认目标版本，并保留配置项用于后续切换。

## 已实现原型能力

当前仓库已经具备以下 FastAPI REST 原型能力：

- `notion-mcp init`、`set-token`、`set-user`、`show`、`run` 的 legacy CLI。
- `~/.notion_mcp/config.json` 或 `NOTION_MCP_CONFIG` 指定路径的 token/user_id 配置读写。
- FastAPI 根路由健康检查。
- 少量 REST 路由：
  - 数据库/数据源列表、详情、查询。
  - 页面获取、创建、更新。
  - 区块子元素列表、追加、更新。
- mock 单元测试覆盖 legacy 配置、CLI 和 REST 路由。
- 仓库已迁移到 `src/notion_mcp/` 可安装布局，并修复隔离安装入口。

以上能力只能证明当前 FastAPI REST 原型可运行，不代表最终 MCP 服务器完成。

## 待实现目标能力（当前已实现）

最终目标是：

```text
Core + CLI + MCP Tool
```

业务调用关系必须是：

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

当前实现状态：

- Core 是唯一业务逻辑层。
- CLI 只负责人类 git-like 使用体验。
- MCP Tool 只负责 Agent/LLM 的结构化调用。
- CLI 和 MCP Tool 都调用 Core，不通过 CLI 字符串绕行。
- MCP Tool 使用真正 MCP server/tool 结构，可被 MCP client 枚举和调用。
- 本地安装支持 `uv` 隔离运行。
- 全局配置支持 token、用户名、Notion 用户 UUID、Notion API version、默认 transport。
- `user_id` 用于本地审计、操作元数据和 auth validate 的用户匹配。
- Notion SDK/API 公开能力按对象域覆盖，并通过受控 raw/pass-through 入口补齐未专门封装的操作：
  - pages
  - blocks
  - databases
  - data sources
  - users
  - comments
  - views
  - file uploads
  - search
  - custom emojis
  - 受控 raw/pass-through 操作入口

发布前验收已经通过；详细执行命令和结果保存在开发进度文档中。

## 当前产品层目标

当前产品层目标：

- 引入 Git-like 本地目录上下文：全局配置继续保存 token、用户和运行参数；项目级 `.notion_mcp/config.json` 只保存项目上下文，不保存 token。
- 支持 page/database attach state：`.notion_mcp/state/page.attach.json` 和 `.notion_mcp/state/database.attach.json`。
- 普通用户围绕 `page` CLI 读取和编辑当前页面内容；`block` CLI 保留为高级/底层入口。
- 严格区分 `database` 和 `data_source`：`database` 是容器对象，`data_source` 是 database 下的具体表。
- 用户 CLI 可保留 `database` 心智，但必须暴露 `data-source` 命名空间，并在多 data source 场景要求显式选择。
- Raw API 保留为兜底和高级入口，不作为普通 page/database 编辑的常用路径。
- Notion-Version 由全局配置集中管理，默认 pinned，不在 Core、CLI 或 MCP tool 模块中硬编码。

## 非功能需求

- 所有功能先写测试，再写实现。
- 已有测试不能为了通过而修改；覆盖不足时新增更明确的补充测试，并在开发进度文档中记录原因。
- 开发者文档和使用者文档必须分离。
- 不允许超大文本文件。
- 源码和测试必须按功能、目的和层次拆分。
- 配置中的 token 默认不得在普通输出中明文泄露。
- 真实 Notion 环境测试默认跳过，必须声明启用条件。
- 不能伪造 live 测试通过。

## 文档边界

- 开发计划、架构决议和测试策略记录在开发文档目录中。
- `Docs/Developer/`：开发者对象文档，包含架构、Core API、MCP tools、测试策略和 packaging。
- `Docs/User/`：使用者对象文档，包含安装、配置、CLI、MCP client 和排障。

## 真实环境约束

以下能力可能需要真实 token、测试 workspace、Notion AI、付费计划或企业权限：

- AI 搜索和跨数据源查询。
- 文件上传。
- 团队、团队空间或高级权限相关接口。
- 对页面、数据库、评论、视图的真实写入。

这些内容必须通过 `live` 测试标记默认跳过；只有显式提供环境变量和测试资源时才能运行。
