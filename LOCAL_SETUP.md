# Local PostgreSQL runtime

`scripts/run_local.py` starts the real FastAPI application on
http://127.0.0.1:8000; interactive API documentation is at `/docs`.
It loads `.local/runtime.env` and `.env.local` without printing secrets.

The current workstation has a dedicated container `retrieval-local-20261008`
and persistent volume of the same name, with PostgreSQL/pgvector on
127.0.0.1:55433. Its schema was initialized using the existing migration
`examples/providers/supabase/migrations/20230414142107_init_pg_vector.sql`.
It is independent from the pharmacy databases.

For a fresh machine provision PostgreSQL with pgvector, apply that migration
once, and set `DATASTORE=postgres`, `PG_HOST`, `PG_PORT`, `PG_DB`, `PG_USER`,
`PG_PASSWORD`, and a random `BEARER_TOKEN` in `.local/runtime.env`.

Install `tests/security/requirements.txt` plus `requirements-local.txt` in an
isolated virtual environment, then run `python scripts/run_local.py`.
This is a verified PostgreSQL subset on Python 3.12, not a compatibility claim
for all optional database providers or the original Poetry dependency lock.

Set `OPENAI_API_KEY` in `.env.local` to enable real embedding ingestion/search.
Without it only API startup, authentication, schema and database connectivity
have been verified. No fake embeddings are substituted.
Keep all credential files local; do not upload them to GitHub or send them in chat.

Stop/start the database with `docker stop retrieval-local-20261008` and
`docker start retrieval-local-20261008`. Do not remove its volume to restart.
