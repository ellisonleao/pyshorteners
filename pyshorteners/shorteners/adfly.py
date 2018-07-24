import json

from ..exceptions import ShorteningErrorException, BadAPIResponseException
from ..base import BaseShortener


class Shortener(BaseShortener):
    """Adf.ly implementation

    Args:
        api_key: adf.ly API key
        user_id: adf.ly user id
        domain: Optional string for domain used upon shortening. Options are:

            - ad.fly
            - q.gs
            - custom.com
            - 0 (Random domain)

        type: Optional string for advertising on the shortened link. Options are:

            - 'int', 'interstitial', 1 for Interstitial advertising
            - 'banner', 3 for Framed Banner
            - 2 , for no Advertising

        group_id: Optional integer param for group_id

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener(api_key='YOUR_KEY', user_id='USER_ID',
                                       domain='test.us', group_id=12, type='int')
        >>> s.adfly.short('http://www.google.com')
        'http://test.us/TEST'
    """
    api_url = 'http://api.adf.ly/'

    def short(self, url):
        """Short implementation for Adf.ly
        Args:
            url: the URL you want to shorten

        Returns:
            A string containing the shortened URL

        Raises:
            BadAPIResponseException: If the data is malformed or we got a bad
            status code on API response
            ShorteningErrorException: If the API Returns an error as response
        """
        url = self.clean_url(url)
        shorten_url = f'{self.api_url}v1/shorten'
        payload = {
            'domain': getattr(self, 'domain', 'adf.ly'),
            'advert_type': getattr(self, 'type', 'int'),
            'group_id': getattr(self, 'group_id', None),
            'key': self.api_key,
            'user_id': self.user_id,
            'url': url,
        }
        response = self._post(shorten_url, data=payload)
        if not response.ok:
            raise BadAPIResponseException(response.content)

        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise BadAPIResponseException('API response could not be decoded')

        if data.get('errors'):
            errors = ','.join(i['msg'] for i in data['errors'])
            raise ShorteningErrorException(errors)

        if not data.get('data'):
            raise BadAPIResponseException(response.content)

        return data['data'][0]['short_url']

    def expand(self, url):
        """Expand implementation for Adf.ly
        Args:
            url: the URL you want to expand

        Returns:
            A string containing the expanded URL

        Raises:
            BadAPIResponseException: If the data is malformed or we got a bad
            status code on API response
            ShorteningErrorException: If the API Returns an error as response
        """
        url = self.clean_url(url)
        expand_url = f'{self.api_url}v1/expand'
        payload = {
            'domain': getattr(self, 'domain', 'adf.ly'),
            'advert_type': getattr(self, 'type', 'int'),
            'group_id': getattr(self, 'group_id', None),
            'key': self.api_key,
            'user_id': self.user_id,
            'url': url,
        }
        response = self._post(expand_url, data=payload)
        if not response.ok:
            raise BadAPIResponseException(response.content)

        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise BadAPIResponseException('API response could not be decoded')

        if data.get('errors'):
            errors = ','.join(i['msg'] for i in data['errors'])
            raise ShorteningErrorException(errors)

        if not data.get('data'):
            raise BadAPIResponseException(response.content)

        return data['data'][0]['url']
