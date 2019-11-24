import json
from pyshorteners.base import BaseShortener
from pyshorteners.exceptions import BadAPIResponseException


class Shortener(BaseShortener):

    """
    Implementation of https://cutt.ly/ URL shortner
    Params Needed :API key

    
    They too provide analyitcs for the URL 
    that you shortened Features to get analytics will be implemented when the author
    approves this PR
    """

    api_url = 'https://cutt.ly/api/api.php '

    def short(self, url, api_key=None):
            if api_key is None:
                return "Please provide a Valid API key"
            url = self.clean_url(url)
            payload = {
                'key': api_key,
                'short': url,

            }
            response = self._get(api_url, params=payload)
            if not response.ok:
                raise BadAPIResponseException(response.content)
            try:
                data = response.json()
            except json.decoder.JSONDecodeError:
                raise BadAPIResponseException("API response is invalid ,could not be decoded")
            return data['url']['shortLink']


s = Shortener()
s.short("https://www.google.com", '9dbec7f1cf9dfa513775d585cde579d677fd6')
print(s)
