from fastapi.testclient import TestClient

from notion_mcp.server import app, get_notion_client


class FakePages:
    def retrieve(self, page_id: str):
        return {"id": page_id, "object": "page"}

    def create(self, **body):
        # echo back parent/data_source_id for testing
        return {"id": "new-page", "body": body}

    def update(self, page_id: str, **body):
        return {"id": page_id, "updated": True, "body": body}


class FakeClient:
    def __init__(self):
        self.pages = FakePages()


def override_get_client() -> FakeClient:
    return FakeClient()


def test_get_page():
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    resp = client.get("/pages/abc")
    assert resp.status_code == 200
    assert resp.json()["id"] == "abc"


def test_create_page():
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    payload = {
        "parent": {"data_source_id": "db1"},
        "properties": {
            "Name": {"title": [{"text": {"content": "Test"}}]}
        },
    }
    resp = client.post("/pages", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "new-page"
    assert data["body"]["parent"]["data_source_id"] == "db1"


def test_update_page():
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    payload = {
        "properties": {
            "Status": {"select": {"name": "Done"}},
        }
    }
    resp = client.patch("/pages/abc", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "abc"
    assert data["updated"] is True