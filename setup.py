#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="antigravity-cli",
    version="2.0.0",
    author="AABH-AI",
    description="AI-powered development platform for Termux — build apps with natural language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AABH-AI/antigravity-cli",
    packages=find_packages(),
    python_requires=">=3.8",
    # Zero external dependencies — uses Python stdlib (urllib, json, pathlib)
    install_requires=[],
    entry_points={
        "console_scripts": [
            "antigravity=antigravity.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    keywords="termux android ai gemini github cli code-generation",
)
