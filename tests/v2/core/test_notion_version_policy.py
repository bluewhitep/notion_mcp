import json
from pathlib import Path
from uuid import uuid4

from notion_mcp.core.client import NotionClientFactory
from notion_mcp.core.config import DEFAULT_NOTION_VERSION, CoreConfig, load_core_config, save_core_config


class CapturingNotionClient:
    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs


def test_default_notion_version_is_pinned() -> None:
    config = CoreConfig()

    assert config.notion_version == DEFAULT_NOTION_VERSION
    assert DEFAULT_NOTION_VERSION == "2026-03-11"


def test_configured_notion_version_is_loaded_from_global_config(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    save_core_config(
        CoreConfig(
            notion_token="secret-token",
            user_name="Ada",
            user_id=str(uuid4()),
            notion_version="2025-09-03",
        ),
        path=config_path,
    )

    loaded = load_core_config(path=config_path)

    assert loaded.notion_version == "2025-09-03"
    assert json.loads(config_path.read_text(encoding="utf-8"))["notion_version"] == "2025-09-03"


def test_notion_client_factory_injects_only_configured_version() -> None:
    config = CoreConfig(notion_token="secret-token", notion_version="2025-09-03")
    factory = NotionClientFactory(client_cls=CapturingNotionClient)

    client = factory.create(config)

    assert client.kwargs["notion_version"] == "2025-09-03"


def test_notion_version_is_not_hardcoded_outside_config_and_tests() -> None:
    forbidden_versions = ["2025-09-03", "2026-03-11"]
    allowed_files = {
        Path("src/notion_mcp/core/config.py"),
        Path("tests/v2/core/test_notion_version_policy.py"),
    }

    for path in Path("src/notion_mcp").rglob("*.py"):
        if path in allowed_files:
            continue
        source = path.read_text(encoding="utf-8")
        for version in forbidden_versions:
            assert version not in source, f"{version} is hardcoded in {path}"
