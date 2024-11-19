import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.download import download_pdb
from src.retrieve_info import retrieve_info
from src.extract_protein import extract_protein
from src.calculate_grid import calculate_grid
from src.protonate import protonate
from src.save_file import save_pdbqt

def main(pdb_id):
    # Download the PDB file
    pdb_file = download_pdb(pdb_id)
    
    # Retrieve all the information
    info = retrieve_info(pdb_file)
    
    # Extract the protein (stripped)
    protein = extract_protein(info)
    
    # Calculate the grid coordinates
    grid_coords = calculate_grid(protein)
    
    # Protonate the protein
    protonated_protein = protonate(protein)
    
    # Save the file into pdbqt format
    save_pdbqt(protonated_protein, pdb_id)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <PDB_ID>")
        sys.exit(1)
    
    pdb_id = sys.argv[1]
    main(pdb_id)
