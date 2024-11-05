import unittest
from unittest.mock import Mock, patch

import requests

from src.pdb_retrival.data_retriever import PDBDataRetriever


class TestPDBDataRetriever(unittest.TestCase):
    @patch("src.pdb_retrival.data_retriever.requests.get")
    def test_fetch_data_success(self, mock_get: Mock) -> None:
        """Test fetch_data method with a successful HTTP response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>Sample HTML Content</html>"
        mock_get.return_value = mock_response

        retriever = PDBDataRetriever("1ABC")
        result = retriever.fetch_data()

        self.assertIsNotNone(result)
        self.assertEqual(result, "<html>Sample HTML Content</html>")
        mock_get.assert_called_once_with(retriever.url, timeout=10)

    @patch("src.pdb_retrival.data_retriever.requests.get")
    def test_fetch_data_failure(self, mock_get: Mock) -> None:
        """Test fetch_data method with a failed HTTP response."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        retriever = PDBDataRetriever("1ABC")
        result = retriever.fetch_data()

        self.assertIsNone(result)
        mock_get.assert_called_once_with(retriever.url, timeout=10)

    def test_parse_data_empty_html(self) -> None:
        """Test parse_data method with empty HTML content."""
        retriever = PDBDataRetriever("1ABC")
        result = retriever.parse_data("")

        self.assertIsInstance(result, dict)
        self.assertIsNone(result["experiment_data"]["method"])
        self.assertIsNone(result["experiment_data"]["resolution"])
        self.assertIsNone(result["experiment_data"]["release_date"])

    @patch("src.pdb_retrival.data_retriever.requests.get")
    def test_get_experiment_method(self, mock_bs: Mock) -> None:
        """Test _get_experiment_method method."""
        mock_soup = Mock()
        mock_method_tag = Mock()
        mock_method_tag.strong = Mock()
        mock_method_tag.text = "Method: X-RAY DIFFRACTION"
        mock_method_tag.strong.text = "Method:"

        mock_soup.find.return_value = mock_method_tag
        retriever = PDBDataRetriever("1ABC")
        result = retriever.get_experiment_method(mock_soup)

        self.assertEqual(result, "X-RAY DIFFRACTION")

    @patch("src.pdb_retrival.data_retriever.requests.get")
    def test_get_resolution(self, mock_bs: Mock) -> None:
        """Test _get_resolution method."""
        mock_soup = Mock()
        mock_resolution_tag = Mock()
        mock_resolution_tag.strong = Mock()
        mock_resolution_tag.text = "Resolution: 1.62 Å"
        mock_resolution_tag.strong.text = "Resolution:"

        mock_soup.find.return_value = mock_resolution_tag
        retriever = PDBDataRetriever("1ABC")
        result = retriever.get_resolution(mock_soup)

        self.assertEqual(result, "1.62 Å")

    @patch("src.pdb_retrival.data_retriever.requests.get")
    def test_get_release_date(self, mock_bs: Mock) -> None:
        """Test _get_release_date method."""
        mock_soup = Mock()
        mock_release_tag = Mock()
        mock_release_tag.stripped_strings = iter(
            ["Deposited:", "2001-01-01", "Released:", "2001-02-01"]
        )

        mock_soup.find.return_value = mock_release_tag
        retriever = PDBDataRetriever("1ABC")
        result = retriever.get_release_date(mock_soup)

        self.assertEqual(result, "2001-02-01")

    def test_is_date_format(self) -> None:
        """Test _is_date_format method."""
        retriever = PDBDataRetriever("1ABC")
        self.assertTrue(retriever.is_date_format("2024-01-01"))
        self.assertFalse(retriever.is_date_format("01-01-2024"))
        self.assertFalse(retriever.is_date_format("Not a date"))

    @patch("src.pdb_retrival.data_retriever.requests.get")
    def test_get_macromolecule_name(self, mock_bs: Mock) -> None:
        """Test _get_macromolecule_name method."""
        mock_soup = Mock()
        mock_row = Mock()
        mock_td = Mock()
        mock_td.text = "Sample Macromolecule Name"

        mock_row.find.return_value = mock_td
        mock_soup.find.return_value = mock_row

        retriever = PDBDataRetriever("1ABC")
        result = retriever.get_macromolecule_name(mock_soup)

        self.assertEqual(result, "Sample Macromolecule Name")


if __name__ == "__main__":
    unittest.main()
