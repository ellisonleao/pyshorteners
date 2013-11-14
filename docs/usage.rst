Usage
=====

To a proper use of pyshorteners, you must first choose the shortener API on objects creation like the example:

    from pyshorteners.shortener import Shortener
    shortener = Shortener('NameOfShortenerAPI', **kwargs)
    
On the `kwargs` dict you can pass auth parameters based on API's requirements. On the Current API's section we show some examples of each one's usage. 
