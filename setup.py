from setuptools import setup, find_packages

setup(
    name="quantum_crypto",
    version="0.1.0",
    package_dir={"": "quantum_crypto/src"},
    packages=find_packages(where="quantum_crypto/src"),
    install_requires=[
        "numpy",
        "cryptography",
    ],
    python_requires=">=3.9",
)
