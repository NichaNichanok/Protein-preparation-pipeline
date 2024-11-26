"""
This module processes PDB files and performs protonation and conversion to PDBQT format.

The main function processes PDB files in the specified input directory, extracts
relevant information, and then performs protonation and conversion to PDBQT
format for each file.
"""

import os

from src.pdbqt_preparation.extract_protein import process_pdb_files
from src.pdbqt_preparation.protonation import protonate_and_convert


def main():
    """
    Main function to process PDB files and perform protonation and conversion to PDBQT
    format.

    This function processes PDB files in the specified input directory, extracts
    relevant information, and then performs protonation and conversion to PDBQT
    format for each file.
    """
    input_path = "./data/raw/test_structure_docking/test_pdbqt_prep"
    output_directory = "./data/raw/test_structure_docking/test_pdbqt_prep"

    # Convert to absolute paths
    input_path = os.path.abspath(input_path)
    output_directory = os.path.abspath(output_directory)

    print('Processing PDB files...')
    processed_files: list[str] = process_pdb_files(input_path, output_directory)
    print(f"Your output directory:{output_directory}")
    print('PDB files processing is done!')

    print('Protonation and conversion is starting!')

    for input_file in processed_files:
        # Only protonate the ".pdb" file
        if input_file.endswith('.pdb'):
            print("\n\n")
            print(len(processed_files))
            print(f"Your input file for the protonation in pdbqt format: {input_file}")
            # Convert to absolute path
            input_path_protonate = f"{output_directory}/{input_file}"
            print("Your input_file_path for the protonation in pdbqt format: "
                  f"{input_path_protonate}")
            output_pdbqt_file = protonate_and_convert(
                input_path_protonate, output_directory
            )
            print(f'Protonation and conversion is done: {output_pdbqt_file}')


if __name__ == "__main__":
    main()
