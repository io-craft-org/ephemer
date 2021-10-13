# coding: utf-8

"""
Setup for ephemer deployment

For sdist deployments, do not forget MANIFEST.in file to include all the data files.
"""

from setuptools import find_packages, setup

import ephemer

setup(
    name="ephemer-django",
    version=ephemer.VERSION,
    description="Ephemer application",
    packages=find_packages(),
    include_package_data=True,
    author="Ephemer",
    author_email="glibersat@iocraft.org",
    url="http://ephemer.iocraft.org",
)
