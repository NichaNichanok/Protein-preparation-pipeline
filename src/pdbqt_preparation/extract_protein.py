import os
from typing import Dict, List

import pymol  # type: ignore
from pymol import cmd  # type: ignore


def initialize_pymol():
    """
    Initialize PyMOL with quiet and no GUI settings.
    """
    pymol.pymol_argv = ['pymol', '-qc']  # type: ignore
    pymol.finish_launching()  # type: ignore


def strip_protein_extract_coordinate_info(input_path: str,
                                          filename: str,
                                          output_directory: str):
    """
    Process a single PDB file: identify ligand center, remove non-protein atoms,
    and save the modified file.

    Args:
    - input_path (str): Path to the input PDB file.
    - filename (str): Name of the PDB file.
    - output_directory (str): Directory to save the modified file.
    """
    pdb_file_path = os.path.join(input_path, filename)
    pdb_file_name = os.path.splitext(filename)[0]

    cmd.load(pdb_file_path, pdb_file_name)  # type: ignore

    # Extract organic molecules in dict format
    organic_molecules = get_organic_molecules(pdb_file_path)
    print("Extract organic molecules:")
    print(organic_molecules)

    # Select and calculate center of mass for each organic molecule and
    # store the center of mass in a separate dictionary
    center_of_mass_dict: Dict[str, List[List[float]]] = {}
    for residue_name, instances in organic_molecules.items():
        center_of_mass_dict[residue_name] = []
        for chain_id, residue_number in instances:
            center_of_mass = calculate_center_of_mass(residue_name,
                                                      chain_id,
                                                      residue_number)
            print(f"Center of mass for {residue_name} in chain {chain_id} at "
                  f"residue {residue_number}: {center_of_mass}")
            center_of_mass_dict[residue_name].append(center_of_mass)

    # Remove non-protein atoms
    cmd.remove("not polymer.protein")  # type: ignore

    protein_center_of_mass = calculate_protein_center_of_mass()
    print(f"Center of mass for protein: {protein_center_of_mass}")
    center_of_mass_dict["protein"] = [protein_center_of_mass]

    print("Extract organic molecules with coordinates:")
    print(center_of_mass_dict)

    # Write grid coordinates to config file
    save_grid_coordinates(output_directory, pdb_file_name, center_of_mass_dict)

    # Save the modified PDB file
    save_modified_structure(output_directory, filename, pdb_file_name)
    print(f"Processed {filename}. Output saved to {output_directory}")


def get_organic_molecules(pdb_file_path: str) -> Dict[str, List[tuple[str, str]]]:
    """
    Extract the organic molecules from a PDB file by searching for the HET record type.

    Args:
        pdb_file_path (str): Full path to the PDB file.
    Returns:
        Dict[str, List[tuple[str, str]]]: Dictionary with residue names as keys and
        lists of (chain, residue number) tuples as values.
    """
    organic_molecules: Dict[str, List[tuple[str, str]]] = {}

    with open(pdb_file_path, "r") as pdb_file:
        pdb_lines = pdb_file.readlines()

    for line in pdb_lines:
        if line.startswith("HET "):
            parts = line.split()

            # Check if the line has enough parts to access
            if len(parts) > 4:
                residue_name = parts[1]
                chain_id = parts[2]
                residue_number = parts[3]
                if len(parts) == 4:
                    residue_name = parts[1]
                    chain_id = parts[2][0]
                    residue_number = parts[2][1:]
                # Append each instance of the organic molecule to the dictionary
                if residue_name not in organic_molecules:
                    organic_molecules[residue_name] = []
                organic_molecules[residue_name].append((chain_id, residue_number))
            else:
                print(f"Warning: Skipping malformed HET line: {line.strip()}")

    if not organic_molecules:
        raise ValueError("No organic molecules found in the PDB file.")

    return organic_molecules


def calculate_center_of_mass(residue_name: str,
                             chain_id: str,
                             residue_number: str) -> List[float]:
    """
    Selects the ligand and calculates its center of mass.

    Args:
    - residue_name (str): Residue name of the organic molecule.
    - chain_id (str): Chain ID where the residue is located.
    - residue_number (str): Residue number of the organic molecule.

    Returns:
    - List[float]: Center of mass coordinates (x, y, z).
    """
    selection_name = f"{residue_name}_{chain_id}_{residue_number}"
    selection_expression = (
        f"(resn {residue_name} and chain {chain_id} and resi {residue_number})"
    )
    cmd.select(selection_name, selection_expression)  # type: ignore
    return cmd.centerofmass(selection_name)  # type: ignore


def calculate_protein_center_of_mass() -> List[float]:
    """
    Calculate the center of mass of the protein itself.

    Args:
    - object_name (str): Name of the loaded object in PyMOL.

    Returns:
    - List[float]: Center of mass coordinates (x, y, z) for the protein.
    """
    cmd.select("protein_structure", "all")  # type: ignore
    return cmd.centerofmass("protein_structure")  # type: ignore


def save_grid_coordinates(output_directory: str,
                          pdb_file_name: str,
                          center_of_mass_dict: Dict[str, List[List[float]]]):
    """
    Save the coordinates of the ligand's center of mass to a config file.

    Args:
    - output_directory (str): Directory for the config file.
    - pdb_file_name (str): Name of the original PDB file.
    - center_of_mass_dict (Dict[str, List[List[float]]]): Center of mass
    coordinates for each organic molecule.
    """
    # Create config file path with modified name
    base_name = os.path.splitext(pdb_file_name)[0]
    config_path = os.path.join(output_directory, f"config_{base_name}.txt")

    with open(config_path, "w") as config_file:
        for residue_name, coordinates_list in center_of_mass_dict.items():
            for center_of_mass in coordinates_list:
                config_file.write(
                    f"Grid coordinates for ligand '{residue_name}' in '{base_name}':\n"
                )
                config_file.write("X: {:.3f}\n".format(center_of_mass[0]))
                config_file.write("Y: {:.3f}\n".format(center_of_mass[1]))
                config_file.write("Z: {:.3f}\n".format(center_of_mass[2]))
                config_file.write("\n")


def save_modified_structure(output_directory: str, filename: str, object_name: str):
    """
    Save the modified PDB structure file after removing non-protein atoms.

    Args:
    - output_directory (str): Directory to save the modified PDB file.
    - filename (str): Original file name for creating the modified file name.
    - object_name (str): Name of the object in PyMOL.
    """
    output_filename = os.path.splitext(filename)[0] + "_stripped.pdb"
    output_file_path = os.path.join(output_directory, output_filename)
    cmd.save(output_file_path, object_name, format="pdb")  # type: ignore


def process_pdb_files(input_path: str, output_directory: str) -> List[str]:
    """
    Process all experimental PDB files in the input directory:
    - Identify the ligand and its center of mass for grid coordinates.
    - Remove non-protein atoms.
    - Save modified files in the output directory.

    Args:
    - input_path (str): Path to the directory containing PDB files.
    - output_directory (str): Path to the directory for saving modified PDB files.
    """
    initialize_pymol()

    processed_files = []
    for filename in os.listdir(input_path):
        processed_files.append(filename)  # type: ignore
        if filename.endswith(".pdb"):
            try:
                strip_protein_extract_coordinate_info(input_path,
                                                      filename,
                                                      output_directory)
                print(f"You {filename} file is stripped and grid coordinates "
                      "are extracted!")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    pymol.cmd.quit()
    return processed_files  # type: ignore


if __name__ == "__main__":
    input_path = (
        "./data/raw/test_pdbqt_prep"
    )
    output_directory = (
        "./data/raw/test_pdbqt_prep"
    )
    process_pdb_files(input_path, output_directory)
