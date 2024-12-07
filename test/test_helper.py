import unittest
import keibascraper
from unittest.mock import patch


class TestHelperSQL(unittest.TestCase):

    @patch('keibascraper.helper.load_config')
    def test_create_table_sql(self, mock_load_config):
        # モックされたJSONデータ
        mock_load_config.return_value = {
            "columns": [
                {"col_name": "bracket", "var_type": "integer"},
                {"col_name": "horse_number", "var_type": "integer"},
                {"col_name": "horse_name", "var_type": "text"},
                {"col_name": "id", "var_type": "text"},

            ]
        }

        # テスト実行
        result = keibascraper.create_table_sql("entry")

        # 期待されるSQL
        expected_sql = (
            "CREATE TABLE IF NOT EXISTS entry ("
            "bracket integer, "
            "horse_number integer, "
            "horse_name text, "
            "id text PRIMARY KEY);"            
        )

        # 検証
        self.assertEqual(result, expected_sql)

    def test_create_index_sql_entry(self):
        # entry データタイプ用のテスト
        result = keibascraper.create_index_sql("entry")

        # 期待されるSQL
        expected_sql = (
            "CREATE INDEX IF NOT EXISTS race_id ON ENTRY (race_id); "
            "CREATE INDEX IF NOT EXISTS horse_id ON ENTRY (horse_id);"
        )

        # 検証
        self.assertEqual(result, expected_sql)

    def test_create_index_sql_result(self):
        # result データタイプ用のテスト
        result = keibascraper.create_index_sql("result")

        # 期待されるSQL
        expected_sql = (
            "CREATE INDEX IF NOT EXISTS race_id ON RESULT (race_id);"
            "CREATE INDEX IF NOT EXISTS horse_id ON RESULT (horse_id);"
        )

        # 検証
        self.assertEqual(result, expected_sql)

    def test_create_index_sql_invalid_type(self):
        # 無効なデータタイプのテスト
        with self.assertRaises(ValueError) as context:
            keibascraper.create_index_sql("invalid_type")

        # エラーメッセージを確認
        self.assertEqual(str(context.exception), "Unexpected data type: invalid_type")

if __name__ == "__main__":
    unittest.main()
