<h1 align="center">
    <img src="https://blog.shareaholic.com/wp-content/uploads/2015/06/shortlink.png" alt="logo"/><br>
    pyshorteners
</h1>

<hr/>

<p align="center">
    <a href="https://travis-ci.org/ellisonleao/pyshorteners"><img src="https://travis-ci.org/ellisonleao/pyshorteners.svg?branch=master" alt="Travis"/></a>
    <a href="https://codecov.io/gh/ellisonleao/pyshorteners"><img src="https://codecov.io/gh/ellisonleao/pyshorteners/branch/master/graph/badge.svg" alt=""/></a>
    <a href="https://saythanks.io/to/ellisonleao"><img src="https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg" alt=""/></a>
</p>

A simple URL shortening Python Lib, implementing the most famous shorteners.

# Installing

    pip install pyshorteners

# Testing

	make test

# Usage

## Simple example

```python
import pyshorteners

s = pyshorteners.Shortener()
print(s.tinyurl.short('www.google.com'))
# prints 'http://tinyurl.com/HASH'
```

## Currently Available Shorteners

- adfly
- bitly
- chilpit
- clckru
- dagd
- isgd
- osdb
- owly
- qpsru
- post
- soogd
- tinycc
- tinyurl
- yourls

Please checkout the [docs](http://pyshorteners.readthedocs.io/en/latest/) for more info and examples on how to use them.
