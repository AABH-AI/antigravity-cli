#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="antigravity-cli",
    version="0.1.0",
    author="AntiGravity Contributors",
    description="A lightweight CLI tool for Termux with zero error tolerance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AABH-AI/antigravity-cli",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["psutil>=5.4.0"],
    entry_points={"console_scripts": ["antigravity=antigravity.cli:main"]},
)
