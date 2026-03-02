---
name: dt-getting-started
description: Use when setting up a Python DataTransformer project for the first time, verifying prerequisites, and running the example test.
---

# DT Getting Started — Python

Checkpoint-based first-run setup for a Python DataTransformer project.

## Prerequisites

- Python 3.9+
- Local PostgreSQL (or Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:14`)
- git

## Walkthrough

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Checkpoint:** `python -c "from datasurface.platforms.yellow.testing.datatransformer_local_test import BaseDTLocalTest; print('OK')"` prints `OK`.

### Step 2: Configure Database Credentials

Set environment variables for the test database connection:

```bash
export TEST_DB_CRED_USER=postgres
export TEST_DB_CRED_PASSWORD=postgres
```

Or create a `.env` file (not committed to git):

```
TEST_DB_CRED_USER=postgres
TEST_DB_CRED_PASSWORD=postgres
```

**Checkpoint:** `psql -h localhost -U postgres -c "SELECT 1"` succeeds (or equivalent connectivity test).

### Step 3: Run Example Tests

```bash
pytest tests/ -v
```

**Checkpoint:** All 4 tests pass:
- `test_basic_passthrough` — rows pass through unchanged
- `test_empty_input` — empty input handled gracefully
- `test_null_values` — NULL values preserved
- `test_output_has_expected_fields` — output schema matches

### Step 4: Understand the Project Structure

Explain to the user:

- **`transformer.py`** — Contains three required functions:
  - `defineInputDatasets()` — What data this DT reads (Datastores with schemas)
  - `defineOutputDatastore()` — What data this DT produces (Datastore with schema)
  - `executeTransformer(connection, dataset_mapping)` — The transformation logic
- **`tests/test_transformer.py`** — Uses `BaseDTLocalTest` which builds a real Ecosystem with local Postgres
- **`requirements.txt`** — Must include `datasurface` plus any libraries your DT needs

### Step 5: Next Steps

Point the user to:
- `/dt-create-transformer` skill to build their own transformer
- [Advanced DT Patterns](https://github.com/datasurface/datasurface/blob/main/docs/DeveloperGuide/150_AdvancedDTPatterns.md) for KV config, self-referencing, ingestion DTs
- [Local DT Development](https://github.com/datasurface/datasurface/blob/main/docs/DeveloperGuide/200_LocalDTDevelopment.md) for the full testing workflow

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ModuleNotFoundError: datasurface` | Run `pip install -r requirements.txt` |
| `connection refused` on port 5432 | Start PostgreSQL or Docker container |
| `FATAL: password authentication failed` | Check `TEST_DB_CRED_USER` and `TEST_DB_CRED_PASSWORD` env vars |
| `ModuleNotFoundError: transformer` | Run pytest from the repo root directory |
