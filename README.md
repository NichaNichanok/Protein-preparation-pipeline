# Protein-preparation-pipeline

This Python package provides an automated pipeline for preparing protein structures for docking studies, including downloading structures, modifying protein files, analyzing binding sites, and calculating grid boxes. The pipeline is designed for use with MGLTools (AutoDock) and offers functionality to support multiple binding sites using clustering methods.

Overview

The Protein-preparation-pipeline package automates key steps in protein structure preparation for computational docking studies. This package enables users to download protein structures, modify them for docking, analyze potential binding sites with clustering methods, and calculate grid boxes based on binding site coordinates for the further virtual screening

Features

The package is divided into four main components:

1.	Download Protein Structure from RCSB PDB Database
	- Fetches protein structures directly from the RCSB Protein Data Bank (PDB) for downstream processing.
2.	Protein Modification in MGLTools (AutoDock)
	- Remove non-protein molecules: Removes water molecules, ions, and other ligands that are not part of the protein backbone.
	- Protonation at physiological pH: Adjusts hydrogen atoms to simulate physiological pH conditions.
	- Save in PDBQT format: Exports the modified protein structure in PDBQT format for compatibility with AutoDock.
3.	Investigation of Binding Sites Using Clustering Methods
   	- Supports multiple binding sites by employing clustering techniques to identify potential regions of interest.
	- Clustering Methods:
		1. QT-clustering: Quick and targeted clustering method for efficient binding site identification.
		2. Spectral clustering: Analyzes similarity matrices for more complex binding site grouping.
4.	Grid Box Calculation for molecular docking 
	- Coordination options:
	    1.	Center of true ligand: Uses the center of the bound ligand as the grid box center.
	    2.	Center of binding residues: Centers on residues critical to the binding pocket.
	- Size: Specifies the grid box size around the selected center.

Validation

The Posebuster dataset is used to validate the pipeline’s effectiveness in preparing proteins and predicting potential binding sites, ensuring reliable and reproducible results.

Note: 

To install this package run one of the following:
conda install conda-forge::pymol-open-source
