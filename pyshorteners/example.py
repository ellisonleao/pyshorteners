# coding: utf-8
from pyshorteners.shortener import Shortener


def hello():
    googl = Shortener('GoogleShortener')

    return """
    Hello World! Testing www.google.com
    Shorten url:{} - Expanded:{}
    """.format(googl.short('http://www.google.com'),
               googl.expand('http://goo.gl/fbsS')),

if __name__ == '__main__':
    hello()
