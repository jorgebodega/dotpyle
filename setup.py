#!/usr/bin/env python
import setuptools

if __name__ == "__main__":
    setuptools.setup()

# -*- coding: utf-8 -*-
# from setuptools import setup, find_packages
# from setuptools.command.install import install
# from subprocess import call
# import os
# import site
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#    
#     def __post_install(self, dir):
#         call(['./dotpyle/autocomplete-install.sh'])
#
#     def run(self):
#         install.run(self)
#
#         self.execute(
#                 self.__post_install,
#                 (self.install_lib,),
#                 msg="Installing auto completion"
#                 )
#
#
#
# # Utility function to read the README file.
# # Used for the long_description.  It's nice, because now 1) we have a top level
# # README file and 2) it's easier to type in the README file than to put a raw
# # string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()
#
# packages = [
#     "dotpyle",
#     "dotpyle.commands",
#     "dotpyle.decorators",
#     "dotpyle.errors",
#     "dotpyle.objects",
#     "dotpyle.services",
#     "dotpyle.templates",
#     "dotpyle.utils",
# ]
#
# package_data = {"": ["*", "*.json", "*.bash", "*.zsh", "*.fish"], "dotpyle": ["templates/*"]}
#
# install_requires = [
#     "Cerberus>=1.3.2,<2.0.0",
#     "GitPython>=3.1.12,<4.0.0",
#     "PyYAML>=5.4.1,<6.0.0",
#     "click>=8.0.1,<9.0.0",
#     "rich>=10.1.0,<11.0.0",
#     "setuptools>=57.4.0,<58.0.0",
# ]
#
# entry_points = {
#     "console_scripts": ["dotpyle = dotpyle.main:main", "test = pytest:main"]
# }
#
#
# setup(
#     name = "dotpyle",
#     version = "0.1.3",
#     description = "Dotfiles manager",
#     long_description = read("README.md"),
#     long_description_content_type = 'text/markdown',
#     author = "Jorge Bodega",
#     author_email = "jorge.bodega.f@gmail.com",
#     maintainer = "Perseo Gutierrez",
#     maintainer_email =  "perseo.gi98@gmail.com",
#     url = "https://github.com/jorgebodega/dotpyle",
#     # "packages = find_packages(where="dotpyle"),
#     packages = packages,
#     package_data = package_data,
#
#     cmdclass = { 'install': PostInstallCommand },
#     include_package_data = True,
#     install_requires = install_requires,
#     entry_points = entry_points,
#     python_requires = ">=3.9,<4.0",
# )
#
