# DataSurface Python DataTransformer Starter

A starter repository for building Python-based DataTransformers with DataSurface.

## Quick Start

Use the AI walkthrough skill for guided setup:

```
/dt-getting-started
```

Or manually:

```bash
pip install -r requirements.txt
export TEST_DB_CRED_USER=postgres
export TEST_DB_CRED_PASSWORD=postgres
pytest tests/ -v
```

## Project Structure

| File | Purpose |
|------|---------|
| `transformer.py` | Your transformation logic — edit this |
| `tests/test_transformer.py` | pytest tests using BaseDTLocalTest |
| `requirements.txt` | Python dependencies |

## How It Works

Your transformer module defines three functions:

1. **`defineInputDatasets()`** — Declares the input Datastores/Datasets your DT reads
2. **`defineOutputDatastore()`** — Declares the output Datastore your DT writes to
3. **`executeTransformer(connection, dataset_mapping)`** — Your transformation logic

DataSurface calls `executeTransformer()` at runtime, passing a SQLAlchemy connection and a `DataTransformerContext` with table mappings, config, and credentials.

## AI Skills

This repo includes Claude Code skills for AI-assisted development:

| Skill | Purpose |
|-------|---------|
| `/dt-getting-started` | First-run setup and test verification |
| `/dt-create-transformer` | Guided creation of a new transformer |
| `/dt-promote` | Tag and promote: local → UAT → prod |

## Documentation

- [Developer Guide](https://github.com/datasurface/datasurface/blob/main/docs/DeveloperGuide/README.md)
- [Advanced DT Patterns](https://github.com/datasurface/datasurface/blob/main/docs/DeveloperGuide/150_AdvancedDTPatterns.md)
- [Local DT Development](https://github.com/datasurface/datasurface/blob/main/docs/DeveloperGuide/200_LocalDTDevelopment.md)
