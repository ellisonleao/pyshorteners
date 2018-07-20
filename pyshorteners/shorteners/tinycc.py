import logging
from ..exceptions import (ShorteningErrorException, ExpandingErrorException,
                          BadAPIResponseException)
from ..base import BaseShortener

logger = logging.getLogger(__name__)


class Shortener(BaseShortener):
    api_url = 'http://tiny.cc/'
    params = {
        'c': 'rest_api',
        'version': '2.0.3',
        'format': 'json',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux) Gecko/20100101 '
                      'Firefox/61.0',
    }

    def short(self, url):
        url = self.clean_url(url)
        params = self.params.copy()
        params.update({
            'm': 'shorten',
            'longUrl': url,
            'login': self.login,
            'apiKey': self.api_key
        })
        response = self._get(self.api_url, params=params, headers=self.headers)
        if not response.ok:
            raise ShorteningErrorException(response.content)

        data = response.json()
        if not data.get('results'):
            raise ShorteningErrorException(data['errorMessage'])

        return data['results']['short_url'].strip()

    def expand(self, url):
        url = self.clean_url(url)
        params = self.params.copy()
        params.update({
            'm': 'expand',
            'longUrl': url,
            'login': self.login,
            'apiKey': self.api_key
        })
        response = self._get(self.api_url, params=params, headers=self.headers)
        if not response.ok:
            raise ExpandingErrorException(response.content)

        data = response.json()
        if not data.get('results'):
            raise ExpandingErrorException(data['errorMessage'])

        return data['results']['longUrl'].strip()

    def total_clicks(self, url):
        url = self.clean_url(url)
        params = self.params.copy()
        params.update({
            'm': 'total_visits',
            'shortUrl': url,
            'login': self.login,
            'apiKey': self.api_key
        })
        response = self._get(self.api_url, params=params, headers=self.headers)
        if not response.ok:
            raise BadAPIResponseException(response.content)

        data = response.json()
        if not data.get('results'):
            raise BadAPIResponseException(data['errorMessage'])

        try:
            total_clicks = int(data['results']['clicks'])
        except (KeyError, TypeError) as e:
            logger.warning('Bad value from total_clicks response: %s', e)
            return 0
        return total_clicks
