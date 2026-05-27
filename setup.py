#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="antigravity-cli",
    version="1.0.0",
    author="AntiGravity Contributors",
    description="Termux CLI with Google Drive Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AABH-AI/antigravity-cli",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "antigravity=antigravity.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
)
