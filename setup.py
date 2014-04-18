#!/usr/bin/env python
from setuptools import setup

NAME = 'magpie'
DESCRIPTION = 'magpie: [ma]rkdown, [g]it, [pie]thon'
VERSION = open('VERSION').read().strip()
LONG_DESC = open('README.rst').read()
LICENSE = open('LICENSE').read()

setup(
    name=NAME,
    version=VERSION,
    author='Charles Thomas',
    author_email='ch@rlesthom.as',
    packages=[],
    url='https://github.com/charlesthomas/%s' % NAME,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    scripts=[],
    classifiers=[]
)
