from setuptools import find_packages, setup

setup(
    name="protein_preparation_pipeline",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
)
