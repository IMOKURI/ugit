#!/usr/bin/env python3

from setuptools import setup

setup(
    name="ugit",
    version="0.1",
    packages=["ugit"],
    entry_points={"console_scripts": ["ugit = ugit.cli:main"]},
)
