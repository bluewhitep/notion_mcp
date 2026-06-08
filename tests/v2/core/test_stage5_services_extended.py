from notion_mcp.core.services.comments import CommentsService
from notion_mcp.core.services.custom_emojis import CustomEmojisService
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


def test_file_upload_list_and_custom_emoji_retrieve() -> None:
    client = FakeClient()

    FileUploadsService(client).list(page_size=5, start_cursor="cursor-1")
    CustomEmojisService(client).retrieve("emoji-1")

    assert client.file_uploads.calls[-1] == (
        "list",
        {"page_size": 5, "start_cursor": "cursor-1"},
    )
    assert client.custom_emojis.calls[-1] == ("retrieve", {"custom_emoji_id": "emoji-1"})
