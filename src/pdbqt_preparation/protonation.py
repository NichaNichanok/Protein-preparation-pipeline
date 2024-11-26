"""This is a module for protonation of the protein using pdb2pqr tool.
This code is modified from the original code in the following link:
https://github.com/joramkuntze/ISOKANNtool/tree/main
"""

import os
import subprocess
from typing import Optional


def protonation(input_file: str, output_dir: str, pH_value: float = 7.4) -> str:
    """
    Perform protonation on the input PDB file using pdb2pqr.

    Args:
        input_file (str): Path to the input PDB file.
        pH_value (float): The pH value for protonation. Defaults to 7.4.
        output_dir (str): Directory to save the output files.

    Returns:
        str: Path to the output PDB file.
    """
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_pdb_file = os.path.join(output_dir, f"{base_name}.pdb")

    # Run pdb2pqr
    subprocess.run([
        'pdb2pqr', '--ff=AMBER', '--titration-state-method', 'propka', '--with-ph',
        str(pH_value), input_file, output_pdb_file
    ], check=True)
    print(f'Output PDB file saved at: {output_pdb_file}')
    return output_pdb_file


def pdbfixer(input_pdb_file: str, output_dir: str, pH_value: float = 7.4) -> str:
    # pdbfixer --pdbid=6o0k --add-residues --ph=7.4 --output=pdbfixer_74.pdb
    print(f"Starting fixing your file: {input_pdb_file}")
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    print(base_name)
    output_pdb_file = os.path.join(output_dir, f"{base_name}.pdb")
    subprocess.run(["pdbfixer",
                    input_pdb_file,
                    "--add-atoms=all",
                    "--add-residues",
                    f"--ph={pH_value}",
                    "--verbose",
                    f"--output={output_pdb_file}"])
    print(f'Your PDB file is protonated at {pH_value} and fixed: {output_pdb_file}')
    return output_pdb_file


def save_pdb2pdbqt(input_pdb_file: str, output_dir: Optional[str] = None) -> str:
    """
    Convert the PDB file to PDBQT format using Open Babel.

    Args:
        input_pDB_file (str): Path to the input PQR file.
        output_dir (Optional[str]): Directory to save the output files. Defaults to the
        input file directory.

    Returns:
        str: Path to the output PDBQT file.
    """
    if output_dir is None:
        output_dir = os.path.dirname(input_pdb_file)

    base_name = os.path.splitext(os.path.basename(input_pdb_file))[0]
    output_pdbqt_file = os.path.join(output_dir, f"{base_name}.pdbqt")

    # Convert PDB to PDBQT using Open Babel
    subprocess.run([
        'obabel', input_pdb_file, '-xr', '-O', output_pdbqt_file
    ], check=True)
    print(f'Output PDBQT file saved at: {output_pdbqt_file}')
    return output_pdbqt_file

# obabel pdbfixer_74_keep_none.pdb -xr -O pdbfixer_obable.pdbqt


def protonate_and_convert(input_file: str,
                          output_dir: str,
                          pH_value: float = 7.4) -> str:
    """
    Perform protonation on the input PDB file and convert the output to PDBQT format.

    Args:
        input_file (str): Path to the input PDB file.
        pH_value (float): The pH value for protonation.
        output_dir (str): Directory to save the output files.

    Returns:
        str: Path to the output PDBQT file.
    """
    # Perform protonation
    output_pdb_file = pdbfixer(input_file, output_dir, pH_value)
    # Convert PQR to PDBQT
    output_pdbqt_file = save_pdb2pdbqt(output_pdb_file, output_dir)
    return output_pdbqt_file


if __name__ == '__main__':
    print('Protonation and conversion is starting!')
    input_file = '/Users/nicha/dev/Protein-preparation-pipeline/data/raw/test_pdbqt_prep/6o0k_stripped.pdb'
    output_dir = './data/raw/test_pdbqt_prep'
    pH_value = 7.0
    output_pdbqt_file = protonate_and_convert(input_file, output_dir, pH_value)
    # pdbfixer(output_pdbqt_file, output_pdbqt_file)
    print(f'Output PDBQT file saved at: {output_pdbqt_file}')
