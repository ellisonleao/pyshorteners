from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    hidelinks.com shortener implementation

    Example:
        >>> import pyshorteners
        >>> s = pyshorteners.Shortener()
        >>> s.hidelinkscom.short('http://www.google.com')
        'http://www.hidelinks.com/?TEST'
    """

    api_url = "https://www.hidelinks.com/convertURL.asp"

    def short(self, url):
        """Short implementation for hidelinks.com

        Args:
            url: the URL you want to shorten

        Returns:
            A string containing the shortened URL

        Raises:
            ShorteningErrorException: If the API returns an error as response
        """
        url = self.clean_url(url)
        data = f'codedURL=&URLData={url}&pwd=&butShortenLink=Shorten+Link%21&pwd_repeat='
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'referer': 'https://www.hidelinks.com/',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'content-length': str(len(data))
        }

        response = self._post(self.api_url, headers=headers, data=data)
        if response.ok:
            return response.text.strip().split('Your shortened link is: <a href=\\"')[1].split('\\"')[0]
        raise ShorteningErrorException(response.content)
