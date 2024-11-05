import re
from typing import Optional

import requests  # type: ignore

PDB_DOWNLOAD_URL = "https://files.wwpdb.org/download/{pdb_id}.pdb"


def validate_pdb_id(pdb_id: str) -> bool:
    """
    Validates the PDB ID to ensure it follows the correct format.

    Args:
        pdb_id (str): PDB ID to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.fullmatch(r"^[A-Z0-9]{4}$", pdb_id, re.IGNORECASE))


def get_pdb(pdb_id: str) -> Optional[str]:
    """
    Downloads the protein structure from the RCSB website by PDB ID.

    Args:
        pdb_id (str): 4-letter PDB code from the RCSB website.

    Returns:
        str: Filename of the downloaded PDB file.

    Raises:
        ValueError: If the PDB file cannot be downloaded.
    """
    if not validate_pdb_id(pdb_id):
        raise ValueError("Invalid PDB ID format: It must be a 4-letter PDB code.")

    pdb_url = PDB_DOWNLOAD_URL.format(pdb_id=pdb_id)
    try:
        response = requests.get(pdb_url,
                                timeout=10)
        response.raise_for_status()
        pdb_filename = f"{pdb_id}.pdb"
        with open(pdb_filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded file in your current path: {pdb_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDB file: {e}")


if __name__ == "__main__":
    pdb_id = "000o"
    get_pdb(pdb_id)
