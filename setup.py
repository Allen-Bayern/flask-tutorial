#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name = "flaskr",
    version = "1.0.1",
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires=["Flask"],
)