from nilo.core.services.pages import PagesService

COMPACT_PAGE_ID = "3799a1afb97a80489bb0e7384f334958"
CANONICAL_PAGE_ID = "3799a1af-b97a-8048-9bb0-e7384f334958"
PAGE_URL = f"https://www.notion.so/Notion-MCP-{COMPACT_PAGE_ID}?source=copy_link"


class FakeChildren:
    def __init__(self, calls: list[tuple[str, dict[str, object]]]) -> None:
        self.calls = calls

    def list(self, **kwargs: object) -> dict[str, object]:
        block_id = str(kwargs["block_id"])
        self.calls.append(("blocks.children.list", kwargs))
        if block_id == "page-1":
            return {
                "object": "list",
                "results": [
                    {
                        "object": "block",
                        "id": "block-1",
                        "type": "paragraph",
                        "parent": {"type": "page_id", "page_id": "page-1"},
                        "has_children": True,
                        "paragraph": {"rich_text": [{"plain_text": "Intro"}]},
                    }
                ],
                "has_more": False,
                "next_cursor": None,
            }
        return {
            "object": "list",
            "results": [
                {
                    "object": "block",
                    "id": "block-2",
                    "type": "bulleted_list_item",
                    "parent": {"type": "block_id", "block_id": "block-1"},
                    "has_children": False,
                    "bulleted_list_item": {"rich_text": [{"plain_text": "Child"}]},
                }
            ],
            "has_more": False,
            "next_cursor": None,
        }


class FakeBlocks:
    def __init__(self, calls: list[tuple[str, dict[str, object]]]) -> None:
        self.children = FakeChildren(calls)


class FakePages:
    def __init__(self, calls: list[tuple[str, dict[str, object]]]) -> None:
        self.calls = calls

    def retrieve(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("pages.retrieve", kwargs))
        return {
            "object": "page",
            "id": kwargs["page_id"],
            "properties": {
                "title": {
                    "type": "title",
                    "title": [{"plain_text": "Project Home"}],
                }
            },
        }


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.pages = FakePages(self.calls)
        self.blocks = FakeBlocks(self.calls)


def test_pages_service_content_returns_flat_block_summary() -> None:
    client = FakeClient()

    result = PagesService(client).content("page-1")

    assert result["page"]["id"] == "page-1"
    assert result["page"]["title"] == "Project Home"
    assert result["blocks"] == [
        {
            "id": "block-1",
            "type": "paragraph",
            "text": "Intro",
            "parent_id": "page-1",
            "has_children": True,
            "children": [],
        }
    ]
    assert client.calls == [
        ("pages.retrieve", {"page_id": "page-1"}),
        ("blocks.children.list", {"block_id": "page-1"}),
    ]


def test_pages_service_content_tree_recursively_reads_children() -> None:
    client = FakeClient()

    result = PagesService(client).content("page-1", tree=True)

    assert result["blocks"][0]["children"] == [
        {
            "id": "block-2",
            "type": "bulleted_list_item",
            "text": "Child",
            "parent_id": "block-1",
            "has_children": False,
            "children": [],
        }
    ]
    assert client.calls == [
        ("pages.retrieve", {"page_id": "page-1"}),
        ("blocks.children.list", {"block_id": "page-1"}),
        ("blocks.children.list", {"block_id": "block-1"}),
    ]


def test_pages_service_retrieve_accepts_copied_notion_url() -> None:
    client = FakeClient()

    result = PagesService(client).retrieve(PAGE_URL)

    assert result["id"] == CANONICAL_PAGE_ID
    assert client.calls == [("pages.retrieve", {"page_id": CANONICAL_PAGE_ID})]
