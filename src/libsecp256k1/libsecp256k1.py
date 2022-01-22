import os
import sys
import ctypes
from ctypes import (
	c_int, c_uint, c_char_p, c_size_t, c_void_p
)
from .utils.dockerhelper import DockerHelper
from .utils.crawler import Crawler

SECP256K1_FLAGS_TYPE_MASK = ((1 << 8) - 1)
SECP256K1_FLAGS_TYPE_CONTEXT = (1 << 0)
SECP256K1_FLAGS_TYPE_COMPRESSION = (1 << 1)

# /** The higher bits contain the actual data. Do not use directly. */
SECP256K1_FLAGS_BIT_CONTEXT_VERIFY = (1 << 8)
SECP256K1_FLAGS_BIT_CONTEXT_SIGN = (1 << 9)
SECP256K1_FLAGS_BIT_COMPRESSION = (1 << 8)

# /** Flags to pass to secp256k1_context_create. */
SECP256K1_CONTEXT_VERIFY = (SECP256K1_FLAGS_TYPE_CONTEXT | SECP256K1_FLAGS_BIT_CONTEXT_VERIFY)
SECP256K1_CONTEXT_SIGN = (SECP256K1_FLAGS_TYPE_CONTEXT | SECP256K1_FLAGS_BIT_CONTEXT_SIGN)
SECP256K1_CONTEXT_NONE = (SECP256K1_FLAGS_TYPE_CONTEXT)

SECP256K1_EC_COMPRESSED = (SECP256K1_FLAGS_TYPE_COMPRESSION | SECP256K1_FLAGS_BIT_COMPRESSION)
SECP256K1_EC_UNCOMPRESSED = (SECP256K1_FLAGS_TYPE_COMPRESSION)

class LibModuleMissing(Exception): pass

class Libsecp265k1:

	def get_lib_path(self, filepath: str):
		return Crawler.joinpath(os.path.dirname(__file__), filepath)

	def unix(self):
		return self.get_lib_path('compiled/unix/libsecp256k1.so.0')

	def win32(self):
		return self.get_lib_path('compiled/win32/libsecp256k1-0.dll')

	def win64(self):
		return self.get_lib_path('compiled/win64/libsecp256k1-0.dll')

	def docker_compile(self):
		# Docker:
		#sudo apt-get update
		#sudo apt install docker.io

		#sudo docker version
		#sudo docker images
		#sudo docker build -t libsecp-builder .
		#sudo docker run -it --rm -v "`pwd`/build:/libsecp/compiled" --name libsecp-builder-instance libsecp-builder
		#sudo docker run hello-docker
		print(DockerHelper.build(self.get_lib_path('docker'), '-t libsecp-builder'))

	def load_library(self):
		if sys.platform in ('windows','win32', 'win64'):
			library_paths = (self.win32(), 'libsecp256k1-0.dll')
		elif sys.platform in ():
			library_paths = (self.win64(), 'libsecp256k1-0.dll')
		else:
			library_paths = (self.unix(), 'libsecp256k1.so.0')

		exceptions = []
		secp256k1 = None
		for libpath in library_paths:
			try:
				secp256k1 = ctypes.cdll.LoadLibrary(libpath)
			except BaseException as e:
				exceptions.append(e)
			else:
				break
		if not secp256k1:
			print(f'libsecp256k1 library failed to load. exceptions: {repr(exceptions)}')
			return None

		try:
			secp256k1.secp256k1_context_create.argtypes = [c_uint]
			secp256k1.secp256k1_context_create.restype = c_void_p

			secp256k1.secp256k1_context_randomize.argtypes = [c_void_p, c_char_p]
			secp256k1.secp256k1_context_randomize.restype = c_int

			secp256k1.secp256k1_ec_pubkey_create.argtypes = [c_void_p, c_void_p, c_char_p]
			secp256k1.secp256k1_ec_pubkey_create.restype = c_int

			secp256k1.secp256k1_ecdsa_sign.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_void_p, c_void_p]
			secp256k1.secp256k1_ecdsa_sign.restype = c_int

			secp256k1.secp256k1_ecdsa_verify.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
			secp256k1.secp256k1_ecdsa_verify.restype = c_int

			secp256k1.secp256k1_ec_pubkey_parse.argtypes = [c_void_p, c_char_p, c_char_p, c_size_t]
			secp256k1.secp256k1_ec_pubkey_parse.restype = c_int

			secp256k1.secp256k1_ec_pubkey_serialize.argtypes = [c_void_p, c_char_p, c_void_p, c_char_p, c_uint]
			secp256k1.secp256k1_ec_pubkey_serialize.restype = c_int

			secp256k1.secp256k1_ecdsa_signature_parse_compact.argtypes = [c_void_p, c_char_p, c_char_p]
			secp256k1.secp256k1_ecdsa_signature_parse_compact.restype = c_int

			secp256k1.secp256k1_ecdsa_signature_normalize.argtypes = [c_void_p, c_char_p, c_char_p]
			secp256k1.secp256k1_ecdsa_signature_normalize.restype = c_int

			secp256k1.secp256k1_ecdsa_signature_serialize_compact.argtypes = [c_void_p, c_char_p, c_char_p]
			secp256k1.secp256k1_ecdsa_signature_serialize_compact.restype = c_int

			secp256k1.secp256k1_ecdsa_signature_parse_der.argtypes = [c_void_p, c_char_p, c_char_p, c_size_t]
			secp256k1.secp256k1_ecdsa_signature_parse_der.restype = c_int

			secp256k1.secp256k1_ecdsa_signature_serialize_der.argtypes = [c_void_p, c_char_p, c_void_p, c_char_p]
			secp256k1.secp256k1_ecdsa_signature_serialize_der.restype = c_int

			secp256k1.secp256k1_ec_pubkey_tweak_mul.argtypes = [c_void_p, c_char_p, c_char_p]
			secp256k1.secp256k1_ec_pubkey_tweak_mul.restype = c_int

			secp256k1.secp256k1_ec_pubkey_combine.argtypes = [c_void_p, c_char_p, c_void_p, c_size_t]
			secp256k1.secp256k1_ec_pubkey_combine.restype = c_int

			# --enable-module-recovery
			try:
				secp256k1.secp256k1_ecdsa_recover.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
				secp256k1.secp256k1_ecdsa_recover.restype = c_int

				secp256k1.secp256k1_ecdsa_recoverable_signature_parse_compact.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
				secp256k1.secp256k1_ecdsa_recoverable_signature_parse_compact.restype = c_int
			except (OSError, AttributeError):
				raise LibModuleMissing('libsecp256k1 library found but it was built '
									   'without required module (--enable-module-recovery)')

			secp256k1.ctx = secp256k1.secp256k1_context_create(SECP256K1_CONTEXT_SIGN | SECP256K1_CONTEXT_VERIFY)
			ret = secp256k1.secp256k1_context_randomize(secp256k1.ctx, os.urandom(32))
			if not ret:
				print('secp256k1_context_randomize failed')
				return None

			return secp256k1
		except (OSError, AttributeError) as e:
			print(f'libsecp256k1 library was found and loaded but there was an error when using it: {repr(e)}')
			return None