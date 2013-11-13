# coding: utf8
from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name='pyshorteners',
    version='0.2.5',
    license='MIT',
    description=('A simple URL shortening Python Lib, implementing '
                 'the most famous shorteners.'),
    long_description=open('README.rst').read(),
    author='Ellison Leão',
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
    namespace_packages=['pyshorteners'],
)
