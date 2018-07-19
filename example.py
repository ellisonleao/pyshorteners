#!/usr/bin/env python
from pyshorteners import Shortener


def hello():
    s = Shortener()
    print(f"""
Hello World! Testing Tinyurl shortener with www.google.com URL
Shorten url: {s.tinyurl.short('http://www.google.com')}
""")


if __name__ == '__main__':
    hello()
