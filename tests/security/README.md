# Boundary regressions

`python -m pytest tests/security tests/services -q` exercises parameter binding,
empty-delete rejection, identifier quoting, Milvus literal encoding, and the
request-owned upload stream fixes inherited from PR #1.

The PostgreSQL cursor is mocked; assertions inspect the actual psycopg2 Composable
object and separate bound values. The Milvus encoder is tested without a server.
These 22 passing tests establish local boundary behavior, not provider integration.
The local isolated Python 3.12 test environment uses Pydantic 1 and FastAPI 0.92;
some helper packages are newer than the old application lockfile.
The CI job installs this same focused environment from requirements.txt; it does
not install or certify every provider in the production Poetry lockfile.

The fix parameterizes all PostgreSQL delete filters, quotes dynamic identifiers,
and rejects empty filters. Milvus/Zilliz inherited search/delete filters and IDs
now serialize text literals instead of interpolating quotes into expressions.
Explicit delete_all behavior is unchanged.

Full database-provider tests, native PostgreSQL/Milvus integration and legacy
Python dependency upgrades remain release gates. This project uses a shared
bearer credential; it is not a multi-tenant authorization design. Never expose
the optional no-auth example as if it inherited server/main.py authentication.

References: [psycopg parameter binding](https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries),
[identifier composition](https://www.psycopg.org/docs/sql.html),
[Milvus scalar expressions](https://milvus.io/docs/boolean.md).
