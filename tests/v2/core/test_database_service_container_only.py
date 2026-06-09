from notion_mcp.core.services.databases import DatabasesService


def test_database_service_does_not_expose_table_level_query() -> None:
    assert not hasattr(DatabasesService, "query")
