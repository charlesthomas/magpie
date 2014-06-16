#!/usr/bin/env python
from setuptools import setup

NAME = 'magpie'
DESCRIPTION = 'magpie: [ma]rkdown, [g]it, [pie]thon'

VERSION = open('VERSION').read().strip()
LONG_DESC = open('README.rst').read()
LICENSE = open('LICENSE').read()
REQUIREMENTS = [open('requirements.txt').readlines()]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2.7',
]

PACKAGES=['magpie', 'magpie/config', 'magpie/handler', 'magpie/static',
          'magpie/template']
PACKAGE_DATA={'magpie': ['config/*.cfg', 'static/*', 'template/*.html']}
SCRIPTS=['utils/pdf_scraper.py', 'utils/email_notes.py']

setup(
    name=NAME,
    version=VERSION,
    author='Charles Thomas',
    author_email='ch@rlesthom.as',
    url='https://github.com/charlesthomas/%s' % NAME,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    scripts=SCRIPTS,
    entry_points='''
    [console_scripts]
    magpie = magpie.server:main
    ''',
)
