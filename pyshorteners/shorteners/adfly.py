from ..exceptions import ShorteningErrorException, BadAPIResponseException
from ..base import BaseShortener


class Shortener(BaseShortener):
    """Adf.ly shortener implementation
    required params: api_key, user_id
    optional params:
    - domain:
        - ad.fly
        - q.gs
        - custom.com
        - 0 (Random domain)
    - type:
        - 'int', 'interstitial', 1 for Interstitial advertising
        - 'banner', 3 for Framed Banner
        - 2 , for no Advertising
    - group_id

    Example:

    >>> s = Shortener(api_key='YOUR_KEY', user_id='USER_ID',
    domain='test.us', group_id=12, type='int')
    >>> s.adfly.short('http://www.google.com')
    'http://test.us/TEST'
    """
    api_url = 'http://api.adf.ly/'

    def short(self, url):
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
            raise ShorteningErrorException(response.content)

        data = response.json()
        if data.get('errors'):
            errors = ','.join(i['msg'] for i in data['errors'])
            raise ShorteningErrorException(errors)

        if not data.get('data'):
            raise BadAPIResponseException(response.content)

        return data['data'][0]['short_url']

    def expand(self, url):
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
            raise ShorteningErrorException(response.content)

        data = response.json()
        if data.get('errors'):
            errors = ','.join(i['msg'] for i in data['errors'])
            raise ShorteningErrorException(errors)

        if not data.get('data'):
            raise BadAPIResponseException(response.content)

        return data['data'][0]['url']
