from pyshorteners.base import BaseShortener
from pyshorteners.exceptions import BadURLException, ExpandingErrorException

import pytest
import responses


def test_base_init_params_become_properties():
    b = BaseShortener(a=1, b=2)
    assert b.a == 1
    assert b.b == 2
    # check default params
    assert b.timeout == 2
    assert b.verify is True


def test_base_clean_url_method():
    # good
    url = 'www.google.com'
    assert BaseShortener.clean_url(url) == f'http://{url}'

    # bad
    with pytest.raises(BadURLException):
        BaseShortener.clean_url('http://')


def test_base_expand_method():
    b = BaseShortener()
    url = 'http://httpbin.org/get'
    assert b.expand(url) == url


def test_base_expand_method_bad_response():
    b = BaseShortener()
    with pytest.raises(ExpandingErrorException):
        b.expand('http://httpbin.org/status/400')


def test_base_get_request_bad_url():
    b = BaseShortener()
    url = '.....'
    with pytest.raises(BadURLException):
        b._get(url)


def test_base_post_request():
    b = BaseShortener()
    url = 'http://httpbin.org/status/200'
    assert b._post(url).status_code == 200


def test_base_post_request_bad_url():
    b = BaseShortener()
    url = '.....'
    with pytest.raises(BadURLException):
        b._post(url)


def test_base_short_method_raises_notimplemented():
    b = BaseShortener()
    with pytest.raises(NotImplementedError):
        b.short('http://someurl')
