from notion_mcp.core.services.comments import CommentsService
from notion_mcp.core.services.custom_emojis import CustomEmojisService
from notion_mcp.core.errors import NotionOperationError
from notion_mcp.core.services.file_uploads import FileUploadsService
from notion_mcp.core.services.pages import PagesService
from notion_mcp.core.services.users import UsersService
from notion_mcp.core.services.views import ViewsService


class Recorder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.calls: list[tuple[str, dict[str, object]]] = []

    def retrieve(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("retrieve", kwargs))
        return {"method": f"{self.name}.retrieve", "kwargs": kwargs}

    def list(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("list", kwargs))
        return {"results": [], "has_more": False, "next_cursor": None, "kwargs": kwargs}

    def create(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("create", kwargs))
        return {"method": f"{self.name}.create", "kwargs": kwargs}

    def update(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("update", kwargs))
        return {"method": f"{self.name}.update", "kwargs": kwargs}

    def query(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("query", kwargs))
        return {"method": f"{self.name}.query", "kwargs": kwargs}


class PagesRecorder(Recorder):
    def __init__(self) -> None:
        super().__init__("pages")
        self.properties = Recorder("pages.properties")


class FakeClient:
    def __init__(self) -> None:
        self.pages = PagesRecorder()
        self.users = Recorder("users")
        self.comments = Recorder("comments")
        self.views = Recorder("views")
        self.file_uploads = Recorder("file_uploads")
        self.custom_emojis = Recorder("custom_emojis")


class ViewsWithoutQuery:
    def __init__(self) -> None:
        self.queries = Recorder("views.queries")


class FakeClientWithViewQueries:
    def __init__(self) -> None:
        self.views = ViewsWithoutQuery()


class CustomEmojisWithoutRetrieve:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def list(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("list", kwargs))
        if "start_cursor" not in kwargs:
            return {
                "results": [{"id": "emoji-1", "name": "one", "url": "https://example.com/1.png"}],
                "has_more": True,
                "next_cursor": "cursor-1",
            }
        return {
            "results": [{"id": "emoji-2", "name": "two", "url": "https://example.com/2.png"}],
            "has_more": False,
            "next_cursor": None,
        }


class FakeClientWithListOnlyCustomEmojis:
    def __init__(self) -> None:
        self.custom_emojis = CustomEmojisWithoutRetrieve()


def test_page_property_retrieve_passes_pagination() -> None:
    client = FakeClient()

    result = PagesService(client).retrieve_property_item(
        "page-1",
        "prop-1",
        page_size=25,
        start_cursor="cursor-1",
    )

    assert result["method"] == "pages.properties.retrieve"
    assert client.pages.properties.calls[-1] == (
        "retrieve",
        {
            "page_id": "page-1",
            "property_id": "prop-1",
            "page_size": 25,
            "start_cursor": "cursor-1",
        },
    )


def test_user_list_passes_pagination() -> None:
    client = FakeClient()

    result = UsersService(client).list(page_size=50, start_cursor="cursor-1")

    assert result["has_more"] is False
    assert client.users.calls[-1] == (
        "list",
        {"page_size": 50, "start_cursor": "cursor-1"},
    )


def test_comment_reply_uses_discussion_payload() -> None:
    client = FakeClient()

    CommentsService(client).reply("discussion-1", [{"type": "text"}])

    assert client.comments.calls[-1] == (
        "create",
        {"discussion_id": "discussion-1", "rich_text": [{"type": "text"}]},
    )


def test_views_create_update_query() -> None:
    client = FakeClient()
    service = ViewsService(client)

    service.create({"data_source_id": "ds-1"})
    service.update("view-1", {"name": "Roadmap"})
    service.query("view-1", {"page_size": 10})

    assert client.views.calls[0] == ("create", {"data_source_id": "ds-1"})
    assert client.views.calls[1] == ("update", {"view_id": "view-1", "name": "Roadmap"})
    assert client.views.calls[2] == ("query", {"view_id": "view-1", "page_size": 10})


def test_views_query_uses_queries_create_when_sdk_has_no_query_method() -> None:
    client = FakeClientWithViewQueries()

    ViewsService(client).query("view-1", {"page_size": 10})

    assert client.views.queries.calls[-1] == (
        "create",
        {"view_id": "view-1", "page_size": 10},
    )


def test_file_upload_list_and_custom_emoji_retrieve() -> None:
    client = FakeClient()

    FileUploadsService(client).list(page_size=5, start_cursor="cursor-1")
    CustomEmojisService(client).retrieve("emoji-1")

    assert client.file_uploads.calls[-1] == (
        "list",
        {"page_size": 5, "start_cursor": "cursor-1"},
    )
    assert client.custom_emojis.calls[-1] == ("retrieve", {"custom_emoji_id": "emoji-1"})


def test_custom_emoji_retrieve_falls_back_to_list_lookup() -> None:
    client = FakeClientWithListOnlyCustomEmojis()

    result = CustomEmojisService(client).retrieve("emoji-2")

    assert result["name"] == "two"
    assert client.custom_emojis.calls == [
        ("list", {"page_size": 100}),
        ("list", {"page_size": 100, "start_cursor": "cursor-1"}),
    ]


def test_custom_emoji_retrieve_list_lookup_raises_when_missing() -> None:
    client = FakeClientWithListOnlyCustomEmojis()

    try:
        CustomEmojisService(client).retrieve("missing")
    except NotionOperationError as exc:
        assert exc.details["operation"] == "custom_emojis.retrieve"
    else:
        raise AssertionError("expected NotionOperationError")
