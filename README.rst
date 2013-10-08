============
Pyshorteners
============

.. figure:: https://api.travis-ci.org/ellisonleao/pyshorteners.png
   :align: center
   :alt: Build Status

   Build Status

Description
===========

A simple URL shortening Python Lib, implementing the most famous
shorteners.

Usage
-----

Create a Shortener instance passing the engine as an argument. Google
Shortener is the default engine if no engine param is passed.

Googl Shortener
---------------

No login or api key needed on kwargs

::

    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('GoogleShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://goo.gl/SsadY'
    print "My long url is {}".format(shortener.expand(url))

Bit.ly
------

API Key and login configs needed on kwargs

::

    from pyshorteners import Shortener

    # For Bit.ly you HAVE to provide the login and api key
    login = 'MY_LOGIN'
    api_key = 'MY_API_KEY'

    url = 'http://www.google.com'
    shortener = Shortener('BitlyShortener', bitly_login=login, bitly_api_key=api_key)
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://bit.ly/AvGsb'
    print "My long url is {}".format(shortener.expand(url))

TinyURL Shortener
-----------------

No login or api key needed

::

    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('TinyurlShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://tinyurl.com/ycus76'
    print "My long url is {}".format(shortener.expand(url))

