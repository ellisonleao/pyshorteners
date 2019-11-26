import json
from pyshorteners.base import BaseShortener
from pyshorteners.exceptions import BadAPIResponseException


class Shortener(BaseShortener):

    """
    Implementation of https://cutt.ly/ URL shortner
    Params Needed :API key

    
    They too provide analytics for the URL 
    that you shortened Features to get analytics will be implemented when the author
    approves this PR
    """

    api_url = 'https://cutt.ly/api/api.php '

    def short(self, url):
            if self.api_key is None:
                raise  BadAPIResponseException("Please provide a valid API Key")
            url = self.clean_url(url)
            api_url=f'{api_url}?key={self.api_key}&short={url}'.strip()
            response = self._get(api_url)
            status=response.json()['status']
            if status ==  4:
                ''' According to the API Docs when a status code of 4 is returned with json 
                    an Invalid API Key is provided
                
                '''

                raise BadAPIResponseException("Invalid API Key")
            try:
                data = response.json()
            except json.decoder.JSONDecodeError:
                raise BadAPIResponseException("API response is invalid ,could not be decoded")
            return data['url']['shortLink']


