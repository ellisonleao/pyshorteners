from ..exceptions import ShorteningErrorException, ExpandingErrorException
from ..base import BaseShortener


class Shortener(BaseShortener):
    """
    Googl Shortener Implementation
    Needs a api_key param
    """
    api_url = 'https://www.googleapis.com/urlshortener/v1/url'

    def short(self, url):
        url = self.clean_url(url)
        shorten_url = f'{self.api_url}?key={self.api_key}'
        response = self._post(shorten_url, json={'longUrl': url})
        if not response.ok:
            raise ShorteningErrorException(response.content)

        data = response.json()
        if 'id' not in data:
            return ShorteningErrorException(f'API Returned wrong data: {data}')

        return data['id']

    def expand(self, url):
        url = self.clean_url(url)
        shorten_url = f'{self.api_url}?key={self.api_key}'
        response = self._get(shorten_url, params={'shortUrl': url})

        if not response.ok:
            raise ExpandingErrorException(response.content)

        data = response.json()
        if 'longUrl' not in data:
            return ExpandingErrorException(f'API Returned wrong data: {data}')

        return data['longUrl']
