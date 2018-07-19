#!/usr/bin/env python

from setuptools import setup, find_packages
import pyshorteners

with open('README.md') as r:
    readme = r.read()

setup(
    name='pyshorteners',
    version=pyshorteners.__version__,
    license=pyshorteners.__license__,
    description=('A Python lib to consume the most used shorteners APIs'),
    long_description=readme,
    author=pyshorteners.__author__,
    author_email=pyshorteners.__email__,
    url='https://github.com/ellisonleao/pyshorteners/',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['requests', ],
    packages=find_packages(exclude=['*tests*']),
)
