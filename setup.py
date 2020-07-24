# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in senergy/__init__.py
from senergy import __version__ as version

setup(
	name='senergy',
	version=version,
	description='Inventory Management',
	author='TeamPRO',
	author_email='barathprathosh@groupteampro.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
