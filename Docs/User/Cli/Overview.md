# CLI Overview

本文说明 `nilo` CLI 的通用规则。

## 通用规则

- 查看帮助时，`-h` 与 `--help` 等价，例如 `nilo -h`、`nilo page -h`。
- 大多数读取命令支持 `--json`，用于给脚本或 Agent 读取结构化结果。
- 写入、更新、发送、完成、trash 等有副作用命令优先使用 `--dry-run` 预览请求。
- JSON 参数通过 `--payload`、`--properties` 或 `--arguments` 传入，内容必须是 JSON object。
- `page/pages`、`block/blocks`、`database/databases` 等复数形式是别名；用户文档默认写单数形式。
- 真实调用前，需要先用 `nilo config --global user.token <token>` 设置全局 token，并确保 Notion connection 已被授权访问目标页面、数据库或 workspace 内容。

## JSON 参数示例

```bash
nilo page update <page_id> --payload '{"properties": {}}'
nilo database query --payload '{"page_size": 10}'
nilo raw-api invoke search --arguments '{"query": "Tasks"}' --json
```

## 副作用命令预览

```bash
nilo block append <block_id> --payload '{"children": []}' --dry-run --json
nilo block trash <block_id> --dry-run
```
