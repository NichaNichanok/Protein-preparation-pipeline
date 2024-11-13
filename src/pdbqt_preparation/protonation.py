"""This is a module for protonation of the protein using pdb2pqr tool.
This code is modified from the original code in the following link: https://github.com/joramkuntze/ISOKANNtool/tree/main
"""

import subprocess


def protonation(input_file: str, output_file: str, output_pqr_file: str) -> None:
    subprocess.run([
        'pdb2pqr', '--ff=AMBER', '--titration-state-method', 'propka', 
        '--with-ph=7.4', '--pdb-output', output_file, input_file, output_pqr_file
    ], check=True)

if __name__ == '__main__':
    input_file = '/Users/nicha/dev/Protein-preparation-pipeline/data/raw/test/6o0k_stripped.pdb'
    output_file = '/Users/nicha/dev/Protein-preparation-pipeline/data/raw/test/6o0k_stripped_pqr.pdb'
    output_pqr_file = '/Users/nicha/dev/Protein-preparation-pipeline/data/raw/test/6o0k_stripped_pqr.pqr'
    protonation(input_file, output_file, output_pqr_file)
    print('Protonation is done!')
