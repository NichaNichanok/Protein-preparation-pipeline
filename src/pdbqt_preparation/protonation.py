"""This is a module for protonation of the protein using pdb2pqr tool.
This code is modified from the original code in the following link:
https://github.com/joramkuntze/ISOKANNtool/tree/main
"""

import os
import subprocess
from typing import Optional


def protonation(input_file: str, pH_value: float, output_dir: str) -> str:
    """
    Perform protonation on the input PDB file using pdb2pqr.

    Args:
        input_file (str): Path to the input PDB file.
        pH_value (float): The pH value for protonation.
        output_dir (str): Directory to save the output files.

    Returns:
        str: Path to the output PQR file.
    """
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_pqr_file = os.path.join(output_dir, f"{base_name}.pqr")

    # Run pdb2pqr
    subprocess.run([
        'pdb2pqr', '--ff=AMBER', '--titration-state-method', 'propka', '--with-ph',
        str(pH_value), input_file, output_pqr_file
    ], check=True)
    print(f'Output PQR file saved at: {output_pqr_file}')
    return output_pqr_file


def save_pqr2pdbqt(input_pqr_file: str, output_dir: Optional[str] = None) -> str:
    """
    Convert the PQR file to PDBQT format using Open Babel.

    Args:
        input_pqr_file (str): Path to the input PQR file.
        output_dir (Optional[str]): Directory to save the output files. Defaults to the
        input file directory.

    Returns:
        str: Path to the output PDBQT file.
    """
    if output_dir is None:
        output_dir = os.path.dirname(input_pqr_file)

    base_name = os.path.splitext(os.path.basename(input_pqr_file))[0]
    output_pdbqt_file = os.path.join(output_dir, f"{base_name}.pdbqt")

    # Convert PQR to PDBQT using Open Babel
    subprocess.run([
        'obabel', '-ipqr', input_pqr_file, '-opdbqt', '-O', output_pdbqt_file
    ], check=True)
    print(f'Output PDBQT file saved at: {output_pdbqt_file}')
    return output_pdbqt_file


def protonate_and_convert(input_file: str, pH_value: float, output_dir: str) -> str:
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
    output_pqr_file = protonation(input_file, pH_value, output_dir)
    # Convert PQR to PDBQT
    output_pdbqt_file = save_pqr2pdbqt(output_pqr_file, output_dir)
    return output_pdbqt_file


if __name__ == '__main__':
    print('Protonation and conversion is starting!')
    input_file = './data/raw/test_structure_docking/test_pdbqt_prep/6o0k_stripped.pdb'
    output_dir = './data/raw/test_structure_docking/test_pdbqt_prep'
    pH_value = 7.0
    output_pdbqt_file = protonate_and_convert(input_file, pH_value, output_dir)
    print(f'Output PDBQT file saved at: {output_pdbqt_file}')
