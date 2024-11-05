import unittest
from typing import Optional
from unittest.mock import MagicMock, mock_open, patch

import requests

from src.pdb_retrival.downloader import get_pdb, validate_pdb_id


class TestPDBFunctions(unittest.TestCase):

    def test_validate_pdb_id_valid(self) -> None:
        self.assertTrue(validate_pdb_id("1ABC"))
        self.assertTrue(validate_pdb_id("1234"))
        self.assertTrue(validate_pdb_id("abcd"))

    def test_validate_pdb_id_invalid(self) -> None:
        self.assertFalse(validate_pdb_id("ABCDE"))  # Too long
        self.assertFalse(validate_pdb_id("1AB"))    # Too short
        self.assertFalse(validate_pdb_id("12#4"))   # Invalid character

    @patch("requests.get")
    def test_get_pdb_valid_id(self, mock_get: MagicMock) -> None:
        # Mock a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"Mock PDB content"

        with patch("builtins.open", mock_open()) as mocked_file:
            result: Optional[str] = get_pdb("1ABC")
            self.assertIsNone(result)  # get_pdb does not return anything explicitly

            # Check if file was written
            mocked_file.assert_called_once_with("1ABC.pdb", "wb")
            mocked_file().write.assert_called_once_with(b"Mock PDB content")

    @patch("requests.get")
    def test_get_pdb_invalid_id(self, mock_get: MagicMock) -> None:
        with self.assertRaises(ValueError):
            get_pdb("12345")  # Invalid ID, should raise ValueError

    @patch("requests.get")
    def test_get_pdb_download_error(self, mock_get: MagicMock) -> None:
        # Mock a response failure
        mock_get.side_effect = requests.exceptions.RequestException("Mock error")

        with patch("builtins.print") as mock_print:
            result: Optional[str] = get_pdb("1ABC")
            self.assertIsNone(result)
            mock_print.assert_any_call("Failed to download PDB file: Mock error")


if __name__ == "__main__":
    unittest.main()
