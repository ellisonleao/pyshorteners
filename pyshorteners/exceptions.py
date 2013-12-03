# coding: utf-8
from __future__ import unicode_literals


class UnknownShortenerException(Exception):
    pass


class ShorteningErrorException(Exception):
    pass


class ExpandingErrorException(Exception):
    pass
