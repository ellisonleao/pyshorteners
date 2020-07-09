from json import loads

from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
	"""
	tr.link shortener implementation

	Example:
		>>> import pyshorteners
		>>> s = pyshorteners.Shortener()
		>>> s.trlink.short('http://www.google.com')
		'https://tr.link/TEST'
	"""

	api_url = "https://tr.link/api/"

	def short(self, url):
		"""Short implementation for hidelinks.com

		Args:
			url: the URL you want to shorten

		Returns:
			A string containing the shortened URL

		Raises:
			ShorteningErrorException: If the API returns an error as response
		"""
		# headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
		url = self.clean_url(url)
		response = self._get(self.api_url, params={"api": self.api_key, "url": url})
		if response.ok:
			shortened_url = loads(response.text.strip())['shortenedUrl']
			return shortened_url
		raise ShorteningErrorException(response.content)
