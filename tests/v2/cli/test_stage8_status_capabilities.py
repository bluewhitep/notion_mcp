from notion_mcp.cli.commands.status import build_status


def test_status_reports_mcp_server_available_after_stage4() -> None:
    status = build_status()

    capabilities = status["capabilities"]

    assert isinstance(capabilities, dict)
    assert capabilities["core"] is True
    assert capabilities["mcp_server"] is True
