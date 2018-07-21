#!/usr/bin/env python
from setuptools import setup, find_packages

import pyshorteners

with open('README.md') as r:
    README = r.read()

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    ('License :: OSI Approved :: GNU General Public License v3 or '
     'later (GPLv3+)'),
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

SHORT_DESC = 'A Python lib to wrap and consume the most used shorteners APIs'

setup(
    name='pyshorteners',
    version=pyshorteners.__version__,
    license=pyshorteners.__license__,
    description=SHORT_DESC,
    long_description=README,
    long_description_content_type='text/markdown',
    author=pyshorteners.__author__,
    author_email=pyshorteners.__email__,
    python_requires='>=3.6',
    url='https://github.com/ellisonleao/pyshorteners/',
    classifiers=CLASSIFIERS,
    install_requires=['requests', ],
    packages=find_packages(exclude=['*tests*']),
)
