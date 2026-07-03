from fastapi.testclient import TestClient

from nilo.server import app, get_notion_client


class FakeDataSources:
    def retrieve(self, data_source_id: str):
        return {"id": data_source_id, "object": "database"}

    def query(self, data_source_id: str, **payload):
        return {"results": [{"id": "row1", "type": "page"}]}


class FakeDatabases:
    def retrieve(self, database_id: str):
        return {"id": database_id, "object": "database"}

    def query(self, database_id: str, **payload):
        return {"results": []}


class FakeClient:
    def __init__(self):
        self.data_sources = FakeDataSources()
        self.databases = FakeDatabases()

    def search(self, filter):
        # simulate search result
        kind = filter.get("value")
        return {"results": [{"id": f"{kind}-1", "object": kind}]}


def override_get_client() -> FakeClient:
    return FakeClient()


def test_list_databases(monkeypatch):
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    resp = client.get("/databases")
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"][0]["object"] == "data_source"


def test_retrieve_database(monkeypatch):
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    resp = client.get("/databases/mydb")
    assert resp.status_code == 200
    assert resp.json()["id"] == "mydb"


def test_query_database(monkeypatch):
    app.dependency_overrides[get_notion_client] = override_get_client
    client = TestClient(app)
    resp = client.post("/databases/mydb/query", json={"filter": {"property": "Name"}})
    assert resp.status_code == 200
    assert resp.json()["results"][0]["id"] == "row1"