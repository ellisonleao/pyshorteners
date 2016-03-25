0.6.0
=====

Breaking changes on the shorteners classes

* Removing the `Shortener` class on the Shortener classes. Check the README for the new examples
* Adding wp-a.co Shortener #40


0.5.8
=====
* Fix goog.gl shortener

0.5.5
=====
* Add timeout kwarg #9

0.5.3
=====
* add `debug` kwarg on Shortener class
* implemented `total_clicks` method on BaseShortener class.
* implemented `total_clicks` on BitlyShortener
* change BitlyShortener `short` and `expand` to use GET requests
* BitlyShortener only requires `bitly_token` for shortening/expading/analytics
* 100% Coverage :smiley:


0.5.2
=====
* Fix import shortcut
* add `_get` and `_post` helper methods on BaseShortener


0.5.1
=====
* add import shortcut

0.5
===

* tests running now with pytest
* fix some py3 issues
* Remove GenericExpander in favor of new BaseShortener class
* All shorteners now must inherit from BaseShortener

0.4.2
=====

* Goo.gl now needs an `api_key` in order to short and expand urls
* Bit.ly now needs an extra `bitly_token` in order to short and expand urls

0.4
===
* Ow.ly shortener added
* Readability shortener added

0.3
===
* Add GenericExpander

0.2.10
======


0.2.8
=====
* Remove Dot.tk API
* Add Senta.la API
* Add qr_code methor on Shortener class
* add shorten and expanded properties on Shortener class

0.2.7
=====
* Add custom exceptions
* Add Is.gd API (Issue #7)
* Fix import Shortener on __init__.py
* add show_current_apis function

0.2.6
=====

* Add Dot.Tk shortener API support

0.2.5
=====

* Python 3 support

0.2.4
0.2.3
=====

* Add kwargs on short, expand functions, fixing the credentials params
* Add Adfly shortener
