from notion_mcp.core.identifiers import parse_notion_page_id


COMPACT_PAGE_ID = "3799a1afb97a80489bb0e7384f334958"
CANONICAL_PAGE_ID = "3799a1af-b97a-8048-9bb0-e7384f334958"


def test_parse_notion_page_id_extracts_from_copied_page_url() -> None:
    url = f"https://www.notion.so/Notion-MCP-{COMPACT_PAGE_ID}?source=copy_link"

    assert parse_notion_page_id(url) == CANONICAL_PAGE_ID


def test_parse_notion_page_id_extracts_from_markdown_link() -> None:
    markdown_link = f"[Notion MCP](https://www.notion.so/Notion-MCP-{COMPACT_PAGE_ID}?source=copy_link)"

    assert parse_notion_page_id(markdown_link) == CANONICAL_PAGE_ID


def test_parse_notion_page_id_preserves_non_uuid_inputs() -> None:
    assert parse_notion_page_id("page-1") == "page-1"
