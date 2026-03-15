#!/usr/bin/env python
"""Setup script for freepygame package."""

import os

from setuptools import find_packages, setup


# 读取版本信息
def get_version():
    """从 __init__.py 读取版本号"""
    version_file = os.path.join("freepygame", "__init__.py")
    with open(version_file, encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip("\"'")
    return "0.1.0"


# 读取 README 文件
def get_long_description():
    """读取 README 文件作为长描述"""
    readme_files = ["README.md", "readme.txt"]
    for filename in readme_files:
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as f:
                return f.read()
    return "A Pygame UI controls library providing buttons, text, circles and other widgets"


setup(
    name="freepygame",
    version=get_version(),
    author="freebird",
    author_email="freebird@example.com",
    description="A Pygame UI controls library providing buttons, text, circles and other widgets",
    long_description=get_long_description(),
    long_description_content_type="text/markdown"
    if os.path.exists("README.md")
    else "text/plain",
    url="https://github.com/freebird/freepygame",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: pygame",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="pygame, ui, controls, widgets, buttons, text, circles",
    project_urls={
        "Bug Reports": "https://github.com/freebird/freepygame/issues",
        "Source": "https://github.com/freebird/freepygame",
        "Documentation": "https://github.com/freebird/freepygame#readme",
    },
)
