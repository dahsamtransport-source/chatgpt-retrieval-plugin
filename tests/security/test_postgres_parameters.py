"""Offline SQL-boundary regression tests; no database or provider credentials."""
from unittest.mock import MagicMock, patch

import pytest
from psycopg2 import sql

# Tokenizer downloading is unrelated to SQL composition and must stay offline.
with patch("tiktoken.get_encoding"):
    from datastore.providers.postgres_datastore import PostgresClient
from models.models import DocumentMetadataFilter, Source


@pytest.fixture
def client():
    instance = PostgresClient.__new__(PostgresClient)
    instance.client = MagicMock()
    return instance


def rendered(query):
    # quote_ident normally needs a live libpq connection. Retain real Composable
    # rendering and parameter bindings; substitute identifier quoting only.
    with patch("psycopg2.extensions.quote_ident", side_effect=lambda value, _: '"' + value.replace('"', '""') + '"'):
        return query.as_string(None)


@pytest.mark.asyncio
@pytest.mark.parametrize("field", ["document_id", "source_id", "author", "start_date", "end_date"])
async def test_filter_values_never_become_sql(client, field):
    attack = "x'; DROP TABLE unrelated; --"
    await client.delete_by_filters("documents", DocumentMetadataFilter(**{field: attack}))
    query, values = client.client.cursor.return_value.__enter__.return_value.execute.call_args.args
    assert isinstance(query, sql.Composable)
    assert attack not in rendered(query)
    assert values == (attack,)
    assert rendered(query).count("%s") == 1


@pytest.mark.asyncio
async def test_combined_filter_preserves_values_and_operators(client):
    await client.delete_by_filters("documents", DocumentMetadataFilter(
        document_id="O'Reilly", source=Source.file, source_id="", author="author",
        start_date="2024-01-01", end_date="2024-12-31"))
    query, values = client.client.cursor.return_value.__enter__.return_value.execute.call_args.args
    assert rendered(query) == 'DELETE FROM "documents" WHERE "document_id" = %s AND "source" = %s AND "source_id" = %s AND "author" = %s AND "created_at" >= %s AND "created_at" <= %s'
    assert values == ("O'Reilly", "file", "", "author", "2024-01-01", "2024-12-31")


@pytest.mark.asyncio
async def test_empty_filter_cannot_delete_all(client):
    with pytest.raises(ValueError, match="filter"):
        await client.delete_by_filters("documents", DocumentMetadataFilter())
    client.client.cursor.assert_not_called()


@pytest.mark.asyncio
async def test_empty_id_list_is_noop(client):
    await client.delete_in("documents", "document_id", [])
    client.client.cursor.assert_not_called()


@pytest.mark.asyncio
async def test_identifier_and_id_are_not_executable(client):
    await client.delete_in('documents"; DROP TABLE other; --', "document_id", ["x'); DELETE FROM other; --"])
    query, values = client.client.cursor.return_value.__enter__.return_value.execute.call_args.args
    assert rendered(query) == 'DELETE FROM "documents""; DROP TABLE other; --" WHERE "document_id" IN %s'
    assert values == (("x'); DELETE FROM other; --",),)
