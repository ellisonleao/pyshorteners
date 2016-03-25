# coding: utf-8
from __future__ import print_function

from pyshorteners import Shortener


def hello():
    short = Shortener('Tinyurl')
    print("""
Hello World! Testing TinyurlShortener with www.google.com URL
Shorten url: {}
Expanded: {}
    """.format(short.short('http://www.google.com'),
               short.expand('http://goo.gl/fbsS')))

if __name__ == '__main__':
    hello()
