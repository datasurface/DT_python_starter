---
name: dt-create-transformer
description: Use when creating a new Python DataTransformer, defining input/output schemas, writing transformation logic, and adding tests.
---

# Create a New Python DataTransformer

Guided walkthrough for adding transformation logic to this project.

## Workflow

### Step 1: Understand the User's Data

Ask the user:
1. What input data do you want to transform? (table names, columns, types)
2. What should the output look like? (columns, types, any aggregation/filtering)
3. Does the transformer need external config or credentials?

### Step 2: Update Input Definitions

Edit `defineInputDatasets()` in `transformer.py`:

```python
def defineInputDatasets() -> List[Datastore]:
    return [
        Datastore(
            "YourSourceStore",
            datasets=[
                Dataset(
                    "your_dataset",
                    schema=DDLTable(columns=[
                        DDLColumn("id", Integer(), NullableStatus.NOT_NULLABLE, PrimaryKeyStatus.PK),
                        # Add columns matching your source data
                    ])
                )
            ]
        )
    ]
```

### Step 3: Update Output Definition

Edit `defineOutputDatastore()` in `transformer.py`:

```python
def defineOutputDatastore() -> Datastore:
    return Datastore(
        "YourOutputStore",
        datasets=[
            Dataset(
                "your_output",
                schema=DDLTable(columns=[
                    DDLColumn("id", Integer(), NullableStatus.NOT_NULLABLE, PrimaryKeyStatus.PK),
                    # Add columns matching your output schema
                ])
            )
        ]
    )
```

### Step 4: Write Transformation Logic

Edit `executeTransformer()` in `transformer.py`. Key APIs:

```python
def executeTransformer(connection: Connection, dataset_mapping: DataTransformerContext) -> Optional[Any]:
    # Get input/output table names
    input_mappings = dataset_mapping.getInputTableMappings()
    output_table = dataset_mapping.getOutputTableNameForDataset("your_output")

    # Get config (if using StaticConfigMap or EnvRefConfigMap)
    config = dataset_mapping.getConfig()

    # Get extra credentials (if defined in model)
    api_key = dataset_mapping.getExtraCredential("your_credential")

    # Your SQL/Python transformation
    connection.execute(text(f'INSERT INTO "{output_table}" ...'))
```

### Step 5: Write Tests

Edit `tests/test_transformer.py`:

```python
def test_your_transformation(self) -> None:
    self.inject_data("your_dataset", [
        {"id": 1, "column": "value"},
    ])

    status = self.run_dt_job()
    self.assertEqual(status, JobStatus.DONE)

    output = self.get_output_data("your_output")
    # Assert your transformation logic produced correct results
```

### Step 6: Run Tests

```bash
pytest tests/ -v
```

**Checkpoint:** All tests pass. If not, debug using IDE breakpoints on `executeTransformer()`.

### Step 7: Commit

```bash
git add -A
git commit -m "feat: add <your transformer name>"
```

## Advanced Patterns

For more complex scenarios, see:
- **KV Config**: Use `StaticConfigMap` for config values, access via `dataset_mapping.getConfig()`
- **Self-Referencing**: Consume own output for batch-to-batch state
- **Ingestion DTs**: Pull data from external APIs using extra credentials
- **IUD Mode**: Write only changed records with `__iud_type__` column

See [Advanced DT Patterns](https://github.com/datasurface/datasurface/blob/main/docs/DeveloperGuide/150_AdvancedDTPatterns.md).
