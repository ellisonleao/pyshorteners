pyshorteners
============

[![Build
Status](http://img.shields.io/travis/ellisonleao/pyshorteners.svg)](https://travis-ci.org/ellisonleao/pyshorteners)
[![Number of PyPI
downloads](http://img.shields.io/pypi/dm/pyshorteners.svg)](https://pypi.python.org/pypi/pyshorteners/0.5.3)
[![Code
Health](https://landscape.io/github/ellisonleao/pyshorteners/master/landscape.svg)](https://landscape.io/github/ellisonleao/pyshorteners/master)
[![codecov.io](http://codecov.io/github/ellisonleao/pyshorteners/coverage.svg?branch=master)](http://codecov.io/github/ellisonleao/pyshorteners?branch=master)


# Description

A simple URL shortening Python Lib, implementing the most famous
shorteners.

# Installing

You can install pythorteners by pip or cloning/forking the repository
and just typing

Installing via pip

    pip install pyshorteners

Installing with the cloned/downloaded code

    python setup.py install

# Testing

	make test

# Usage

Create a Shortener instance passing the engine as an argument. Google
Shortener is the default engine if no engine param is passed.

## Goo.gl Shortener

`api_key` needed on kwargs

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
api_key = 'YOUR_API_KEY'
shortener = Shortener('GoogleShortener', api_key=api_key)
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://goo.gl/SsadY'
print "My long url is {}".format(shortener.expand(url))
```

## Bit.ly Shortener

`bitly_token` needed on kwargs

```python
from pyshorteners import Shortener

# For Bit.ly you HAVE to provide the login and api key
access_token = 'MY_ACCESS_TOKEN'

url = 'http://www.google.com'
shortener = Shortener('BitlyShortener', bitly_token=access_token)
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://bit.ly/AvGsb'
print "My long url is {}".format(shortener.expand(url))
```

## TinyURL.com Shortener

No login or api key needed

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('TinyurlShortener')
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://tinyurl.com/ycus76'
print "My long url is {}".format(shortener.expand(url))
```

## Adf.ly Shortener

`uid` and `api_key` needed, Banner `type` optional (`int` or `banner`).
No expanding for this shortener

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('AdflyShortener')
print "My short url is {}".format(shortener.short(url, uid=UID,
                                  api_key=API_KEY, type='int'))
```

## Is.gd Shortener

No login or api key needed

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('IsgdShortener')
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://is.gd/SsaC'
print "My long url is {}".format(shortener.expand(url))
```

## Senta.la Shortener

No login or api key needed

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('SentalaShortener')
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://senta.la/urubu'
print "My long url is {}".format(shortener.expand(url))
```

## Qr.cx Shortener

No login or api key needed

````python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('QrCxShortener')
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://qr.cx/XsC'
print "My long url is {}".format(shortener.expand(url))
```

## Readbility Shortener

No login or api key needed

```python
from pyshorteners import Shortener

url = 'http://blog.arc90.com/2010/11/30/silence-is-golden/'
shortener = Shortener('ReadbilityShortener')
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://rdd.me/ycus76'
print "My long url is {}".format(shortener.expand(url))
```

## Ow.ly Shortener

`api_key` needed on kwargs

```python
from pyshorteners import Shortener

# For Ow.ly you HAVE to provide the login and api key
api_key = 'MY_API_KEY'

url = 'http://www.google.com'
shortener = Shortener('OwlyShortener',api_key=api_key)
print "My short url is {}".format(shortener.short(url))

### expanding
url = 'http://ow.ly/AvGsb'
print "My long url is {}".format(shortener.expand(url))
```

## Osdb.link Shortener

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('OsdbShortener')
print "My short url is {}".format(shortener.short(url))
```

# Generating QR Code

You can have the QR Code for your url by calling the `qr_code` method
after shortening your url.

```python
from pyshorteners import Shortener

url = 'http://www.google.com'
shortener = Shortener('TinyurlShortener')
shortener.short(url)
print shortener.qrcode()

Output
http://chart.apis.google.com/chart?cht=qr&chl=http://tinyurl.com/1c2&chs=120x120
```
Image:

![](http://chart.apis.google.com/chart?cht=qr&chl=http://tinyurl.com/1c2&chs=120x120)


# Creating your own Shortener

To create your shortener handler you will need to:

1. Create a new file on shorteners/ folder (e.g shorteners/myshort.py)
2. Create a MyShortShortener class implementing `short`, `expand` and optionally `total_clicks` methods:

```python
class MyShortShortener(BaseShortener):
	api_url = 'http://myapishortener.com/api'

	def short(self, url):
		pass

	def expand(self, url):
		pass

	def total_clicks(self, url):
		pass
```
3. If you need to pass extra keyword args like a `token` or `api_key` , you will need to handle it on the `__init__()` method.
4. Import this shortener on `shorteners/__init__.py` file
5. Send a PR with a test included
