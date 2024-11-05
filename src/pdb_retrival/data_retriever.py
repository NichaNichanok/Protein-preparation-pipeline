import re
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from src.pdb_retrival.downloader import validate_pdb_id


class PDBDataRetriever:
    """
    Class to retrieve and parse PDB data from the RCSB website.
    """

    def __init__(self, pdb_id: str) -> None:
        """
        Initializes the PDBDataRetriever with a PDB ID.

        Args:
            pdb_id (str): The PDB ID to retrieve data for.

        Raises:
            ValueError: If the PDB ID is not valid.
        """
        if not validate_pdb_id(pdb_id):
            raise ValueError("Invalid PDB ID format: It must be a 4-letter PDB code.")
        self.pdb_id = pdb_id
        self.url = f"https://www.rcsb.org/structure/{pdb_id}"

    def fetch_data(self) -> Optional[str]:
        """
        Fetches the HTML content for the given PDB ID.

        Returns:
            Optional[str]: The HTML content if the request is successful, otherwise
            None.
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data: {e}")
            return None

    def parse_data(self, html_content: str) -> Dict[str, Any]:
        """
        Parses the HTML content to extract various data fields.

        Args:
            html_content (str): The HTML content to parse.

        Returns:
            Dict[str, Any]: A dictionary containing parsed data fields.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        data = {  # type: ignore
            "experiment_data": {
                "method": self._get_experiment_method(soup),
                "resolution": self._get_resolution(soup),
                "release_date": self._get_release_date(soup),
            },
            "macromolecules": {
                "name": self._get_macromolecule_name(soup),
                "total_weight": self._get_size_kda(soup),
                "unique_protein_chains": self._get_unique_chains(soup),
                "classification": self._get_classification(soup),
                "organism": self._get_organism(soup),
                "expression_system": self._get_expression_system(soup),
                "mutation": self._get_mutation(soup),
            },
            "small_molecules": self._get_small_molecules(soup),
        }

        return data  # type: ignore

    def _get_experiment_method(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the experiment method from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The experiment method if found, otherwise None.
        """
        method_tag: Optional[Tag] = soup.find("li",
                                              id="exp_header_0_method")  # type: ignore
        if method_tag is not None and method_tag.strong is not None:
            return method_tag.text.replace(method_tag.strong.text, "").strip()
        else:
            return None

    def _get_resolution(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the resolution from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The resolution if found, otherwise None.
        """
        resolution_tag: Optional[Tag] = soup.find(
            "li", id="exp_header_0_diffraction_resolution")  # type: ignore
        if resolution_tag is not None and resolution_tag.strong is not None:
            return resolution_tag.text.replace(resolution_tag.strong.text, "").strip()
        else:
            return None

    def _get_release_date(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the release date from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The release date in YYYY-MM-DD format if found, otherwise
            None.
        """
        release_date_tag: Optional[Tag] = soup.find(
            "li", id="header_deposited-released-dates"
        )  # type: ignore
        if release_date_tag is not None:
            date_parts: ResultSet[str] = (  # type: ignore
                release_date_tag.stripped_strings)  # type: ignore
            dates = [
                part
                for part in date_parts
                if part.strip() and self._is_date_format(part.strip())
            ]
            if dates:
                return dates[-1].replace("\xa0", "").strip()
        return None

    def _is_date_format(self, text: str) -> bool:
        """
        Checks if the given text matches the YYYY-MM-DD date format.

        Args:
            text (str): The text to check.

        Returns:
            bool: True if the text matches the date format, otherwise False.
        """
        return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", text))

    def _get_macromolecule_name(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the macromolecule name from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The macromolecule name if found, otherwise None.
        """
        macromolecule_row: Optional[Tag] = soup.find(
            "tr", id="macromolecule-entityId-1-rowDescription"
        )  # type: ignore
        if macromolecule_row is not None:
            td_element: Optional[Tag] = macromolecule_row.find("td")  # type: ignore
            if td_element is not None:
                return td_element.text.strip()
        return None

    def _get_size_kda(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the size in kDa from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The size in kDa if found, otherwise None.
        """
        size_tag: Optional[Tag] = soup.find(
            "li", id="contentStructureWeight")  # type: ignore
        if size_tag is not None:
            return size_tag.text.split(":")[1].strip()
        return None

    def _get_unique_chains(self, soup: BeautifulSoup) -> Optional[int]:
        """
        Extracts the number of unique protein chains from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[int]: The number of unique protein chains if found, otherwise None.
        """
        chains_tag: Optional[Tag] = soup.find(
            "li", id="contentProteinChainCount")  # type: ignore
        if chains_tag is not None:
            try:
                return int(chains_tag.text.split(":")[1].strip())
            except (IndexError, ValueError):
                return None
        return None

    def _get_classification(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the classification from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The classification if found, otherwise None.
        """
        classification_tag: Optional[Tag] = soup.find(
            "li", id="header_classification")  # type: ignore
        if classification_tag is not None and classification_tag.find("a") is not None:
            return classification_tag.find("a").text.strip()  # type: ignore
        return None

    def _get_organism(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the organism from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The organism if found, otherwise None.
        """
        organism_tag: Optional[Tag] = soup.find(
            "li", id="header_organism")  # type: ignore
        if organism_tag is not None and organism_tag.find("a") is not None:
            return organism_tag.find("a").text.strip()  # type: ignore
        return None

    def _get_expression_system(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts the expression system from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[str]: The expression system if found, otherwise None.
        """
        expression_system_tag: Optional[Tag] = soup.find(
            "li", id="header_expression-system"
        )  # type: ignore
        if (
            expression_system_tag is not None
            and expression_system_tag.find("a") is not None
        ):
            return expression_system_tag.find("a").text.strip()  # type: ignore
        return None

    def _get_mutation(self, soup: BeautifulSoup) -> Optional[bool]:
        """
        Extracts the mutation status from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[bool]: True if there is a mutation, False if not, and None if not
            found.
        """
        mutation_tag: Optional[Tag] = soup.find("li",
                                                id="header_mutation")  # type: ignore
        if mutation_tag is not None and mutation_tag.strong is not None:
            mutation_text = mutation_tag.text.replace(
                mutation_tag.strong.text, ""
            ).strip()
            return mutation_text.lower() != "no"
        return None

    def _get_small_molecules(self, soup: BeautifulSoup) -> Optional[Dict[str, str]]:
        """
        Extracts small molecules from the HTML content.

        Args:
            soup (BeautifulSoup): The parsed HTML content.

        Returns:
            Optional[Dict[str, str]]: A dictionary with ligand IDs as keys and names as
            values.
        """
        small_molecules_panel: Optional[Tag] = soup.find(
            "div", id="smallMoleculespanel"
        )  # type: ignore
        if small_molecules_panel is not None:
            ligand_rows: ResultSet[Tag] = small_molecules_panel.find_all(
                "tr", id=lambda x: x and x.startswith("ligand_row_")  # type: ignore
            )
            small_molecules: Dict[str, str] = {}

            for row in ligand_rows:
                ligand_id_tag: Optional[Tag] = row.find("a")  # type: ignore
                if ligand_id_tag is not None:
                    ligand_id = ligand_id_tag.text.strip()
                    ligand_name = self._get_small_molecule_name(row)
                    if ligand_name is not None:
                        small_molecules[ligand_id] = ligand_name
                    else:
                        small_molecules[ligand_id] = "Name not found"

            return small_molecules if small_molecules else None
        return None

    def _get_small_molecule_name(self, row: Tag) -> Optional[str]:
        """
        Extracts the name of a small molecule from a table row.

        Args:
            row (Tag): The <tr> element containing the small molecule information.

        Returns:
            Optional[str]: The name of the small molecule if found, otherwise None.
        """
        strong_tag: Optional[Tag] = row.find("strong")  # type: ignore
        if strong_tag is not None:
            return strong_tag.text.strip()
        return None


if __name__ == "__main__":
    retriever = PDBDataRetriever("9RUB")  # Example PDB ID for testing
    html_content = retriever.fetch_data()
    if html_content:
        parsed_data = retriever.parse_data(html_content)
        print(parsed_data)
