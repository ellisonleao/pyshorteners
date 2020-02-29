#!/usr/bin/env python
# pylint: disable=C0114
from setuptools import setup, find_packages

import pyshorteners

with open("README.md") as r:
    README = r.read()

TESTS_REQUIRE = [
    "flake8==3.7.7",
    "responses==0.10.6",
    "pytest==4.4.1",
    "pytest-cov==2.7.1",
    "codecov==2.0.15",
    "pytest-flake8",
]


CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

SHORT_DESC = "A Python lib to wrap and consume the most used shorteners APIs"

setup(
    name="pyshorteners",
    version=pyshorteners.__version__,
    license=pyshorteners.__license__,
    description=SHORT_DESC,
    long_description=README,
    long_description_content_type="text/markdown",
    author=pyshorteners.__author__,
    author_email=pyshorteners.__email__,
    python_requires=">=3.6",
    url="https://github.com/ellisonleao/pyshorteners/",
    classifiers=CLASSIFIERS,
    install_requires=["requests"],
    setup_requires=["pytest-runner"],
    tests_require=TESTS_REQUIRE,
    packages=find_packages(exclude=["*tests*"]),
    extras_require={"dev": ["pre-commit"], "docs": ["sphinx"]},
)
