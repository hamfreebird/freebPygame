import codecs
import os

from setuptools import find_packages, setup

# 读取 README 文件作为长描述
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "readme.txt"), encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本信息
version = {}
with open(os.path.join(here, "freepygame", "__init__.py"), encoding="utf-8") as f:
    exec(f.read(), version)

setup(
    name="freepygame",
    version="0.1.0",
    author="freebird",
    author_email="",
    description="A Pygame UI controls library providing buttons, text, circles and other widgets",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: pygame",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="pygame, ui, controls, widgets, buttons, text, circles",
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.0.0",
    ],
    project_urls={
        "Bug Reports": "",
        "Source": "",
    },
)
