Usage
=====

To a proper use of pyshorteners, you must first choose the shortener API on objects creation like the example:

.. code:: python

    from pyshorteners.shortener import Shortener
    shortener = Shortener('NameOfShortenerAPI', ** kwargs)
    
On the `kwargs` dict you can pass auth parameters based on API's requirements. On the Current API's section we show some examples of each one's usage. 


Example
=======

.. code:: python

    from pyshorteners.shortener import Shortener

    s = Shortener('GoogleShortener')

    short_url = s.short('http://www.google.com')

    print 'My short url is {}'.format(short_url)

    #  You can access the shorten url attributes anytime
    print s.shorten # prints the short url
    print s.expanded # prints the long url

    print s.qr_code() # prints the QR code url for this short url
