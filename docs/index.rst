Welcome to pyshorteners documentation
=====================================

`pyshorteners` is a Python lib to help you short and expand urls using the most famous URL Shorteners availables.

With pyshorteners , generate a short url is as easy as typing

.. code-block:: python

	import pyshorteners

	s = pyshorteners.Shortener()
	print(s.tinyurl.short('http://www.g1.com.br'))


To install pyshorteners just grab it directly from PyPI::

	pip install pyshorteners

Some URL Shortening services have their own set of restrictions and additional params you must provide in order to use it. Right now pyshorteners implements the following APIs:

- adfly
- bitly
- chilpit
- clckru
- dagd
- isgd
- osdb
- owly
- qpsru
- soogd
- tinycc
- tinyurl

Click on each one to get more information about how to use it.

Developing
==========

If you would like to contribute to the project, please make sure to check the `CONTRIBUTING <https://github.com/ellisonleao/pyshorteners/blob/master/CONTRIBUTING.md>`_ section


.. toctree::
	:maxdepth: 2
	:caption: Contents:




