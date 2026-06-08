"""
配置管理模块。

提供读写全局配置文件的函数，包括设置/获取 Notion 集成 token 和当前用户 UUID。配置文件默认保存在
用户主目录下的 ``~/.notion_mcp/config.json``，并可通过环境变量 ``NOTION_MCP_CONFIG`` 覆盖。

在实现时我们使用 Pydantic 模型来序列化/反序列化配置，并确保配置字段完整。若配置文件不存在，
调用 ``load_config`` 时会抛出 ``FileNotFoundError``。设置函数会在不存在配置时创建新配置。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import Config


# 默认配置目录与文件名
DEFAULT_CONFIG_DIR = Path.home() / ".notion_mcp"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"


def get_config_path() -> Path:
    """返回配置文件的路径。

    如果设置了环境变量 ``NOTION_MCP_CONFIG``，则使用其值作为配置文件路径；否则使用默认路径。
    """
    from os import getenv

    env_path = getenv("NOTION_MCP_CONFIG")
    if env_path:
        return Path(env_path).expanduser()
    return DEFAULT_CONFIG_FILE


def load_config(path: Optional[Path] = None) -> Config:
    """读取配置文件并返回 ``Config`` 实例。

    Args:
        path: 配置文件路径，默认为 ``get_config_path()``。

    Returns:
        ``Config``: 解析后的配置对象。

    Raises:
        FileNotFoundError: 当配置文件不存在时抛出。
        json.JSONDecodeError: 当配置文件不是有效 JSON 时抛出。
    """
    cfg_path = path or get_config_path()
    if not cfg_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return Config.model_validate(data)


def save_config(config: Config, path: Optional[Path] = None) -> None:
    """将 ``Config`` 对象序列化到指定路径。

    如果父目录不存在则自动创建。

    Args:
        config: 要保存的配置对象。
        path: 保存路径，默认为 ``get_config_path()``。
    """
    cfg_path = path or get_config_path()
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    data = config.model_dump(exclude_none=True)
    with cfg_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_token(token: str, path: Optional[Path] = None) -> None:
    """更新配置中的 Notion token。

    如果配置文件不存在，则新建配置对象。写入完成后保存到磁盘。
    """
    try:
        cfg = load_config(path)
    except FileNotFoundError:
        cfg = Config()
    cfg.notion_token = token
    save_config(cfg, path)


def set_user(user_id: str, path: Optional[Path] = None) -> None:
    """更新配置中的当前用户 UUID。

    如果配置文件不存在，则新建配置对象。写入完成后保存到磁盘。
    """
    try:
        cfg = load_config(path)
    except FileNotFoundError:
        cfg = Config()
    cfg.user_id = user_id
    save_config(cfg, path)
