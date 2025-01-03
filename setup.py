from setuptools import setup, find_namespace_packages

setup(
    name="dirtree",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        'pyyaml>=6.0.1',
        'tqdm>=4.65.0'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'dirtree=src.cli:main',  # Update entry point to use src package
        ],
    }
)
