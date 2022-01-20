import os
from .utils.crawler import Crawler

class Libsecp256k1:

	@classmethod
	def _get_package_file(self, filepath: str):
		return Crawler.joinpath(os.path.dirname(__file__), filepath)

	@classmethod
	def unix(self):
		return self._get_package_file('compiled/unix/libsecp256k1.so.0')

	@classmethod
	def win32(self):
		return self._get_package_file('compiled/win32/libsecp256k1-0.dll')

	@classmethod
	def win64(self):
		return self._get_package_file('compiled/win64/libsecp256k1-0.dll')
