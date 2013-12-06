Current API's
=============

PyShorteners for now supports these shorteners API's:

## Goo.gl 

* No kwargs needed

Example:

    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('GoogleShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://goo.gl/SsadY'
    print "My long url is {}".format(shortener.expand(url))


## Bit.ly

* API Key and Login needed

Example:

    from pyshorteners import Shortener

    # For Bit.ly you HAVE to provide the login and api key
    login = 'MY_LOGIN'
    api_key = 'MY_API_KEY'

    url = 'http://www.google.com'
    shortener = Shortener('BitlyShortener', bitly_login=login,bitly_api_key=api_key)
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://bit.ly/AvGsb'
    print "My long url is {}".format(shortener.expand(url))

## TinyURL Shortener

* No kwargs needed

Example:


    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('TinyurlShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://tinyurl.com/ycus76'
    print "My long url is {}".format(shortener.expand(url))

## Adf.ly Shortener

* UID and API Key needed
* Optional kwarg **type** (int or banner)

Example:

    from pyshorteners import Shortener
    
    url = 'http://www.google.com'
    shortener = Shortener('AdflyShortener')
    print "My short url is {}".format(shortener.short(url, uid=UID, api_key=API_KEY, type='int'))

## Is.gd Shortener

* No kwargs needed

Example:


    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('IsgdShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://is.gd/AxcA'
    print "My long url is {}".format(shortener.expand(url))

## Senta.la Shortener

* No kwargs needed

Example:


    from pyshorteners import Shortener

    url = 'http://www.google.com'
    shortener = Shortener('SentalaShortener')
    print "My short url is {}".format(shortener.short(url))

    # expanding
    url = 'http://senta.la/urubu'
    print "My long url is {}".format(shortener.expand(url))
