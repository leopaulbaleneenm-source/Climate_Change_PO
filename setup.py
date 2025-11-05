from setuptools import setup, find_packages

setup(
    name="climato_PO",
    version="0.1.0",
    author="BALENE Léo-Paul",
    author_email="leopaul.balene.enm@gmail.com",
    description="Un package pour l'analyse climatique des paramètres météorologiques observés à la station de Rivesaltes",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
    ],
    python_requires=">=3.8",
)