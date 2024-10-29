import requests
from .constants import PDB_DOWNLOAD_URL


def get_pdb(pdb_id):
    """
    Downloads the protein structure from the RCSB website by PDB ID.

    Args:
        pdb_id (str): 4-letter PDB code from the RCSB website.

    Returns:
        str: Filename of the downloaded PDB file.

    Raises:
        ValueError: If the PDB file cannot be downloaded.
    """
    pdb_url = PDB_DOWNLOAD_URL.format(pdb_id=pdb_id)
    response = requests.get(pdb_url)
    if response.status_code == 200:
        pdb_filename = f"{pdb_id}.pdb"
        with open(pdb_filename, 'wb') as f:
            f.write(response.content)
        return pdb_filename
    else:
        raise ValueError(f"Failed to download PDB file for {pdb_id}")
