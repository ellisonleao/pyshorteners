# coding: utf8
from __future__ import unicode_literals

from setuptools import setup, find_packages
import pyshorteners

setup(
    name='pyshorteners',
    version=pyshorteners.__version__,
    license=pyshorteners.__license__,
    description=('A Python lib to consume the most used shorteners APIs'),
    long_description=open('README.md').read(),
    author=pyshorteners.__author__,
    author_email='ellisonleao@gmail.com',
    url='https://github.com/ellisonleao/pyshorteners/',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['requests', ],
    packages=find_packages(exclude=['*tests*']),
)
