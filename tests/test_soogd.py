from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener(suffix="g4de")
short_url = "http://soo.gd/g4de"
expanded = "http://www.test.com"
soo = s.soogd


@responses.activate
def test_soogd_short_method():
    # mock response
    body = (
        '<input onclick="this.select();" name="link1" size="40" '
        'value="http://soo.gd/g4de" dir="ltr">'
    )
    responses.add(responses.POST, soo.api_url, body=body)

    shorten = soo.short(expanded)
    assert shorten == short_url


@responses.activate
def test_soogd_short_method_bad_response():
    responses.add(responses.POST, soo.api_url, body="bad_response", status=400)

    with pytest.raises(ShorteningErrorException):
        soo.short(expanded)


def test_generate_suffix_staticmethod():
    suffix = soo._generate_random_suffix()
    assert len(suffix) == 4
