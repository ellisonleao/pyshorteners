#!/usr/bin/env python
# coding: utf-8
from nose.core import run

if __name__ == '__main__':
    args = ['', '--cover-package=pyshorteners', '--with-coverage']
    run(argv=args)
