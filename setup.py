# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "dotpyle",
    "dotpyle.commands",
    "dotpyle.errors",
    "dotpyle.services",
    "dotpyle.utils",
]

package_data = {"": ["*"], "dotpyle": ["templates/*"]}

install_requires = [
    "Cerberus>=1.3.2,<2.0.0",
    "GitPython>=3.1.12,<4.0.0",
    "PyYAML>=5.4.1,<6.0.0",
    "click>=8.0.1,<9.0.0",
    "rich>=12.4.4,<12.5.0",
    "setuptools>=62.3.2,<62.4.0",
]

entry_points = {
    "console_scripts": ["dotpyle = dotpyle.main:main", "test = pytest:main"]
}

setup_kwargs = {
    "name": "dotpyle",
    "version": "0.1.0",
    "description": "Test",
    "long_description": None,
    "author": "Jorge Bodega",
    "author_email": "jorge.bodega.f@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.9,<4.0",
}


setup(**setup_kwargs)
