from fastapi.testclient import TestClient

from nilo.server import app, get_notion_client


class FakeBlocksChildren:
    def list(self, block_id: str):
        return {"results": ["child1", "child2"]}

    def append(self, block_id: str, **body):
        # pretend to append and return the body
        return {"results": body.get("children", [])}


class FakeBlocks:
    def __init__(self):
        self.children = FakeBlocksChildren()

    def update(self, block_id: str, **body):
        return {"id": block_id, "updated": True, "body": body}


class FakeClient:
    def __init__(self):
        self.blocks = FakeBlocks()


def override_get_client() -> FakeClient:
    return FakeClient()


def test_list_block_children():
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    resp = client.get("/blocks/b1/children")
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"] == ["child1", "child2"]


def test_append_block_children():
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    payload = {"children": ["newchild"]}
    resp = client.post("/blocks/b1/append", json=payload)
    assert resp.status_code == 200
    assert resp.json()["results"] == ["newchild"]


def test_update_block():
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    payload = {"paragraph": {"text": [{"text": {"content": "updated"}}]}}
    resp = client.patch("/blocks/b1", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "b1"
    assert data["updated"] is True