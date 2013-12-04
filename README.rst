============
Pyshorteners
============

.. image:: https://api.travis-ci.org/ellisonleao/pyshorteners.png
   :alt: Build Status
   :target: https://travis-ci.org/ellisonleao/pyshorteners

.. image:: https://pypip.in/v/pyshorteners/badge.png
    :target: https://crate.io/packages/pyshorteners/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/pyshorteners/badge.png
    :target: https://crate.io/packages/pyshorteners/
    :alt: Number of PyPI downloads


Description
===========

A simple URL shortening Python Lib, implementing the most famous
shorteners.


Installing
==========

You can install pythorteners by pip or cloning/forking the repository and just typing

Installing via pip

::

    pip install pyshorteners


Installing with the cloned/downloaded code

::

    python setup.py install

Testing
-------

Use tox to test with all environments needed by just typing `tox` on command line


Usage
=====

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

Adf.ly Shortener
-----------------

uid and api key needed, banner type optional (int or banner)
No expanding for this shortener

::

    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('AdflyShortener')
    print "My short url is {}".format(shortener.short(url, uid=UID,
                                      api_key=API_KEY, type='int'))

Dot.Tk Shortener
-----------------

No login or api key needed

::

    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('DottkShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://0ydtx.tk'
    print "My long url is {}".format(shortener.expand(url))


.. image:: https://d2weczhvl823v0.cloudfront.net/ellisonleao/pyshorteners/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

