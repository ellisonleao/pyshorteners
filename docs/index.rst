Welcome to pyshorteners documentation
=====================================

`pyshorteners` is a Python lib to help you short and expand urls using the most famous URL Shorteners availables.

With pyshorteners , generate a short url or expand another one is as easy as typing

.. code-block:: python

	import pyshorteners

	s = pyshorteners.Shortener()
	print(s.tinyurl.short('http://www.g1.com.br'))


To install pyshorteners just grab it directly from PyPI::

	pip install pyshorteners



Contents
--------

.. toctree::

    apis
    contributing
    apis/modules.rst
