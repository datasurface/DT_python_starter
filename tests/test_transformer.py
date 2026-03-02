"""
Tests for the identity pass-through transformer.

Uses BaseDTLocalTest which builds a real Ecosystem with a local Postgres
database. Tests inject data, run the transformer, and verify output.

Prerequisites:
  - Local PostgreSQL running (default: localhost:5432)
  - Environment variables for credentials:
      TEST_DB_CRED_USER=postgres
      TEST_DB_CRED_PASSWORD=postgres
"""

import unittest
from datasurface.platforms.yellow.testing.datatransformer_local_test import BaseDTLocalTest
from datasurface.platforms.yellow.yellow_states import JobStatus


class TestPassthroughTransformer(BaseDTLocalTest):
    """Test the identity pass-through transformer."""

    def setUp(self) -> None:
        super().setUp()
        self.setup_from_transformer_module(module_path="transformer")

    def test_basic_passthrough(self) -> None:
        """Verify rows pass through unchanged."""
        self.inject_data("records", [
            {"id": 1, "name": "Alice", "value": "alpha"},
            {"id": 2, "name": "Bob", "value": "beta"},
        ])

        status = self.run_dt_job()
        self.assertEqual(status, JobStatus.DONE)

        output = self.get_output_data("records")
        self.assertEqual(len(output), 2)

        # Verify data is unchanged
        names = {row["name"] for row in output}
        self.assertEqual(names, {"Alice", "Bob"})

    def test_empty_input(self) -> None:
        """Verify transformer handles empty input gracefully."""
        self.inject_data("records", [])

        status = self.run_dt_job()
        self.assertEqual(status, JobStatus.DONE)

        self.assert_output_count(0)

    def test_null_values(self) -> None:
        """Verify nullable columns pass through as NULL."""
        self.inject_data("records", [
            {"id": 1, "name": "Charlie", "value": None},
        ])

        status = self.run_dt_job()
        self.assertEqual(status, JobStatus.DONE)

        output = self.get_output_data("records")
        self.assertEqual(len(output), 1)
        self.assertIsNone(output[0]["value"])

    def test_output_has_expected_fields(self) -> None:
        """Verify output schema matches expectations."""
        self.inject_data("records", [
            {"id": 1, "name": "Test", "value": "val"},
        ])

        self.run_dt_job()
        self.assert_output_contains_field("id")
        self.assert_output_contains_field("name")
        self.assert_output_contains_field("value")


if __name__ == "__main__":
    unittest.main()
