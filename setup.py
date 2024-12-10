from setuptools import setup, find_packages

setup(
    name="quantum_crypto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "cryptography",
    ],
    python_requires=">=3.9",
)
