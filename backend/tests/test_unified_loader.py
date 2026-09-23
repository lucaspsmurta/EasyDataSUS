import os
import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch, Mock
from tempfile import TemporaryDirectory


BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from config.datasets import DATASETS_CONFIG
from etl.load_csv import (
    _convert_value,
    _dataset_files,
    _header_mapping,
    load_csv,
    reload_datasets,
    _ensure_srag_columns,
    _preflight,
    _iter_batches,
    SRAG_REQUIRED_COLUMNS,
)


class UnifiedLoaderTests(unittest.TestCase):
    def test_srag_migration_only_adds_missing_columns(self):
        client = Mock()
        with patch("etl.load_csv._table_schema", return_value=[("tp_idade", "Nullable(Int32)")]):
            _ensure_srag_columns(client, ["surtos-srag"])
        self.assertEqual(3, client.command.call_count)
        self.assertTrue(all("ADD COLUMN IF NOT EXISTS" in c.args[0] for c in client.command.call_args_list))
        client.reset_mock()
        with patch("etl.load_csv._table_schema", return_value=list(SRAG_REQUIRED_COLUMNS.items())):
            _ensure_srag_columns(client, ["surtos-srag"])
        client.command.assert_not_called()
        _ensure_srag_columns(client, ["leitos"])
        client.command.assert_not_called()

    def test_new_columns_are_loaded_from_csv(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "srag.csv"
            path.write_text("TP_IDADE;HEMATOLOGI;HEPATICA;NEUROLOGIC\n3;1;2;1\n", encoding="utf-8")
            with patch("etl.load_csv._table_schema", return_value=[]), patch("etl.load_csv._dataset_files", return_value=[path]):
                plan = _preflight(Mock(), ["surtos-srag"])["surtos-srag"]
            _, encoding, mapping = plan["files"][0]
            batches = list(_iter_batches(path, encoding, plan["schema"], mapping, 10))
            self.assertEqual([[(3, 1, 2, 1)]], batches)

    def test_missing_source_fields_abort_before_mutation(self):
        client = Mock()
        with TemporaryDirectory() as directory:
            path = Path(directory) / "srag.csv"
            path.write_text("NU_NOTIFIC\n123\n", encoding="utf-8")
            with patch("etl.load_csv.get_clickhouse_client", return_value=client), patch("etl.load_csv._table_schema", return_value=[("nu_notific", "Int64")]), patch("etl.load_csv._dataset_files", return_value=[path]):
                with self.assertRaisesRegex(ValueError, "campos obrigatórios"):
                    reload_datasets(["surtos-srag"])
            client.command.assert_not_called()
            client.insert.assert_not_called()

    def test_dry_run_does_not_migrate_or_truncate(self):
        client = Mock()
        with patch("etl.load_csv.get_clickhouse_client", return_value=client), patch("etl.load_csv._preflight", return_value={}), patch("etl.load_csv._ensure_srag_columns") as migrate, patch("etl.load_csv._ensure_date32_columns") as dates:
            reload_datasets(["surtos-srag"], dry_run=True)
        migrate.assert_not_called()
        dates.assert_not_called()
        client.command.assert_not_called()

    def test_every_configured_dataset_has_csv(self):
        missing = {
            dataset: _dataset_files(dataset)
            for dataset in DATASETS_CONFIG
            if not _dataset_files(dataset)
        }
        self.assertEqual({}, missing)

    def test_header_mapping_is_case_insensitive(self):
        mapping = _header_mapping(
            ["NU_NOTIFIC", "DT_NOTIFIC", "SG_UF_NOT"],
            [("nu_notific", "Int64"), ("dt_notific", "Date"), ("sg_uf_not", "String")],
        )
        self.assertEqual("NU_NOTIFIC", mapping["nu_notific"])
        self.assertEqual("DT_NOTIFIC", mapping["dt_notific"])

    def test_type_conversion_handles_dates_numbers_and_nulls(self):
        self.assertEqual(date(2026, 7, 4), _convert_value("04/07/2026", "Date"))
        self.assertEqual(12, _convert_value("12.0", "Int32"))
        self.assertEqual(1.5, _convert_value("1,5", "Float64"))
        self.assertIsNone(_convert_value("", "Nullable(String)"))
        self.assertIsNone(_convert_value("01/01/1950", "Nullable(Date)"))
        self.assertEqual(date(1950, 1, 1), _convert_value("01/01/1950", "Nullable(Date32)"))

    def test_no_dataset_means_all_configured_datasets(self):
        with patch("etl.load_csv.reload_datasets") as reload_mock:
            reload_mock.return_value = {}
            load_csv()
        self.assertEqual(list(DATASETS_CONFIG.keys()), reload_mock.call_args.args[0])

    def test_dataset_argument_limits_replacement_scope(self):
        with patch("etl.load_csv.reload_datasets") as reload_mock:
            reload_mock.return_value = {}
            load_csv(dataset="leitos")
        self.assertEqual(["leitos"], reload_mock.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
