# THIS DOC IS FOR THE UPCOMING VERSION. DO NOT USE THE EXAMPLE CODE YET! For the old usage, please refer to [this comment](https://github.com/ellisonleao/pyshorteners/issues/117#issuecomment-471043530)

<h1 align="center">
    <img src="https://blog.shareaholic.com/wp-content/uploads/2015/06/shortlink.png" alt="logo"/><br>
    pyshorteners
</h1>

<hr/>

<p align="center">
    <a href="https://github.com/ellisonleao/pyshorteners/actions"><img src="https://github.com/ellisonleao/pyshorteners/workflows/build/badge.svg" alt="Travis"/></a>
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
- nullpointer
- osdb
- owly
- qpsru
- post
- soogd
- tinycc
- tinyurl
- gitio

Please checkout the [docs](http://pyshorteners.readthedocs.io/en/latest/) for more info and examples on how to use them.
