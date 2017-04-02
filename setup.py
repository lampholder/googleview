# -*- coding: utf-8 -*-
"""It's setup.py, shut up linter."""

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

setup(
    name='googleview',
    version='0.1',
    description='Tool for making it easy to wrangle tabulated data and upload it to Google sheets. \
                 It shouldn\'t need to exist but computering is sometimes hard.',
    long_description=README,
    author='Thomas Lant',
    author_email='lampholder@gmail.com',
    url='https://github.com/lampholder/googleview',
    packages=find_packages(),
    install_requires=['oauth2client', 'pydrive', 'unicodecsv']
)
