from ..exceptions import ShorteningErrorException, BadAPIResponseException
from ..base import BaseShortener


class Shortener(BaseShortener):
    """
    Adf.ly shortener implementation
    Needs api key and uid
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
