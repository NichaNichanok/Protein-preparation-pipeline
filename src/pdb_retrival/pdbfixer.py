import subprocess

def pdbfixer(input, output):
    subprocess.run(["pdbfixer",input, "--add-atoms=all", "--add-residues", "--verbose", f"--output={output}"])
