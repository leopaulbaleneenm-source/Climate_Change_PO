from setuptools import setup, find_packages

setup(
    name="Climate_Change_PO",
    version="0.1.0",
    author="BALENE Léo-Paul",
    author_email="leopaul.balene.enm@gmail.com",
    description="Climatic analysis of meteorological parameters observed at the Rivesaltes station to highlight climate change phenomena.",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
    ],
    python_requires=">=3.8",
)