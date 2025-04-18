#!/usr/bin/env python3
"""
Setup configuration for the CosmicDestiny application
"""

from setuptools import setup, find_packages
import os

# Read requirements
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Read long description from README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cosmic-destiny",
    version="1.0.0",
    description="A comprehensive destiny analysis application using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CosmicDestiny Team",
    author_email="info@cosmicdestiny.example.com",
    url="https://github.com/Dylan0624/CosmicDestiny",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cosmic_destiny": [
            "ui/*.qss",
            "resources/images/*",
            "resources/fonts/*",
        ],
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cosmic-destiny=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)

