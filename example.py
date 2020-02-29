#!/usr/bin/env python
from pyshorteners import Shortener


def hello():
    s = Shortener(timeout=5)
    print(
        f"""
    Hello World! Testing google.com for some shorteners

    Results
    =======
    - TinyURL     - {s.tinyurl.short('http://www.google.com')}
    - Chilp.it    - {s.chilpit.short('http://www.google.com')}
    - Clck.ru     - {s.clckru.short('http://www.google.com')}
    - Da.gd       - {s.dagd.short('http://www.google.com')}
    - Git.io      - {s.gitio.short('https://www.github.com/ellisonleao/sharer.js')}
    - Is.gd       - {s.isgd.short('http://www.google.com')}
    - NullPointer - {s.nullpointer.short('http://www.google.com')}
    - Osdb.link   - {s.osdb.short('http://www.google.com')}
    - Qps.ru      - {s.qpsru.short('www.google.com')}
"""
    )


if __name__ == "__main__":
    hello()
