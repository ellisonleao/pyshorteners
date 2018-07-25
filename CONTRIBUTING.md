CONTRIBUTING to pyshorteners
============================

First of all, thanks for your intention to help with this project. It was built while i was learning some python magic features and it really makes me happy that you also want to be part of this.

Some steps to make our lives easier:

1. Before start making any code changes, please open an issue or check if your feature/bugfix is already being handled.
2. Please always make your changes on a separated branch, you choose the name of it.
3. Please follow PEP8.
4. Make sure `make test` passes before sending the Pull request.

Thanks for your help and let me buy you a :beer: sometime

Building a new Shortener
------------------------

If you want to build another implementation of a shortener API, you basically need to:

1. Create a new module under the `shorteners` folder with the shortener api name (e.g: `adfly.py`)
2. Create a `Shortener` class inheriting from `BaseShortener` (`pyshorteners.base.BaseShortener`)
3. add the `api_url` property with the API url
4. Implement `short` and `expand` methods
5. You can add custom methods if you want. Just make sure to document it.
6. Add docstring for the new `Shortener` class following [Google Style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)

Example:

```python
# yourapi.py
from pyshorteners.base import BaseShortener

class Shortener(BaseShortener):
    """
    Docstring
    """
    api_url = 'http://the/link/for/the/api'

    def short(self, url):
        pass

    def expand(self, url):
        pass

    def custom_method(self):
        pass
```

Then, to use this new shortener, just try:

```python

>>> import pyshorteners
>>> s = Shortener()
>>> s.yourapi.short('http://some.url')
'result'
>>> s.yourapi.expand('http://some.url')
'result2'
>>> s.yourapi.custom_method()
```

Check out the [current implementations](https://github.com/ellisonleao/pyshorteners/tree/master/pyshorteners/shorteners) for more info
