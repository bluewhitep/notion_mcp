import json

from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import pages as page_commands
from nilo.core.services.pages import PagesService
from tests.v2.fixtures.fake_notion import FakeNotionClient


runner = CliRunner()


def test_cli_page_create_flows_to_core_fake_notion(monkeypatch) -> None:
    fake_client = FakeNotionClient()
    monkeypatch.setattr(page_commands, "get_pages_service", lambda: PagesService(fake_client))

    result = runner.invoke(
        app,
        [
            "page",
            "create",
            "--payload",
            '{"parent": {"page_id": "root"}}',
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["object"] == "page"
    assert fake_client.calls[-1] == (
        "pages.create",
        {"parent": {"page_id": "root"}},
    )
