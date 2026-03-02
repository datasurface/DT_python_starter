"""
DataSurface Python DataTransformer - Identity Pass-Through

This is a starter transformer that reads input datasets and writes them
unchanged to the output. Replace the logic in executeTransformer() with
your transformation code.

Required functions:
  - defineInputDatasets(): Returns list of Datastores this DT reads from
  - defineOutputDatastore(): Returns the Datastore this DT writes to
  - executeTransformer(connection, dataset_mapping): Your transformation logic
"""

from typing import Any, List, Optional

from sqlalchemy import text
from sqlalchemy.engine import Connection

from datasurface.md.governance import Datastore, Dataset
from datasurface.md.schema import DDLTable, DDLColumn, NullableStatus, PrimaryKeyStatus
from datasurface.md.types import Integer, VarChar
from datasurface.platforms.yellow.transformer_context import DataTransformerContext


def defineInputDatasets() -> List[Datastore]:
    """Define the input datasets this transformer reads.

    Returns a list of Datastores. Each Datastore contains Datasets
    with schemas matching your source data.
    """
    return [
        Datastore(
            "SampleSource",
            datasets=[
                Dataset(
                    "records",
                    schema=DDLTable(
                        columns=[
                            DDLColumn("id", Integer(), NullableStatus.NOT_NULLABLE, PrimaryKeyStatus.PK),
                            DDLColumn("name", VarChar(100), NullableStatus.NOT_NULLABLE),
                            DDLColumn("value", VarChar(200)),
                        ]
                    )
                )
            ]
        )
    ]


def defineOutputDatastore() -> Datastore:
    """Define the output datastore this transformer writes to.

    The output schema should match what your transformer produces.
    For this pass-through example, it matches the input exactly.
    """
    return Datastore(
        "SampleOutput",
        datasets=[
            Dataset(
                "records",
                schema=DDLTable(
                    columns=[
                        DDLColumn("id", Integer(), NullableStatus.NOT_NULLABLE, PrimaryKeyStatus.PK),
                        DDLColumn("name", VarChar(100), NullableStatus.NOT_NULLABLE),
                        DDLColumn("value", VarChar(200)),
                    ]
                )
            )
        ]
    )


def executeTransformer(connection: Connection, dataset_mapping: DataTransformerContext) -> Optional[Any]:
    """Main entry point called by DataSurface at runtime.

    Args:
        connection: SQLAlchemy Connection to the merge database
        dataset_mapping: DataTransformerContext with table mappings, config, and credentials

    Returns:
        Optional result (usually None)
    """
    # Get input table mappings: logical name -> physical table name
    input_mappings = dataset_mapping.getInputTableMappings()

    # Get the output table name for the "records" dataset
    output_table = dataset_mapping.getOutputTableNameForDataset("records")

    # Find the input table for "records" from SampleSource
    input_table: Optional[str] = None
    for key, table_name in input_mappings.items():
        if "records" in key:
            input_table = table_name
            break

    if input_table is None:
        raise RuntimeError("Input table 'records' not found in mappings")

    # --- Your transformation logic goes here ---
    # This pass-through copies all rows from input to output unchanged.
    # Replace this with your actual transformation.
    sql = (
        f'INSERT INTO "{output_table}" (id, name, value) '
        f'SELECT id, name, value FROM "{input_table}"'
    )
    connection.execute(text(sql))

    return None
