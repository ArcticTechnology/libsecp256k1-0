import os
import sys
import ctypes
import platform
from os.path import isdir
from ctypes import (
	c_int, c_uint, c_char_p, c_size_t, c_void_p
)
from .utils.docker import Docker
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

class Libsecp265k1:

	def get_lib_path(self, filepath: str) -> str:
		return Crawler.joinpath(os.path.dirname(__file__), filepath)

	def unix(self) -> str:
		return self.get_lib_path('compiled/unix/libsecp256k1.so.0')

	def win32bit(self) -> str:
		return self.get_lib_path('compiled/win32bit/libsecp256k1-0.dll')

	def win64bit(self) -> str:
		return self.get_lib_path('compiled/win64bit/libsecp256k1-0.dll')

	def docker_compile(self, outpath: str = None, interactive: bool = False) -> dict:
		if outpath == None:
			compiledpath = self.get_lib_path('compiled')
		else:
			if isdir(outpath) == False:
				message = 'Error: Invalid output path, no action taken.'; print(message)
				return {'status': 400, 'message': message}
			else:
				compiledpath = Crawler.joinpath(outpath, 'compiled')

		if interactive == True and isdir(compiledpath):
			print(' ')
			print('Existing docker compile found: {}'.format(compiledpath))
			print(' ')
			print('Would you like to overwrite this file? [y/n]')
			select = input()
			os.system('clear')
			if select != 'y':
				message = 'Exited, no action taken.'; print(message)
				return {'status': 400, 'message': message}

		dockerpath = self.get_lib_path('docker')
		docker_build = Docker.exec('docker build', '-t', 'libsecp-builder', dockerpath)
		if docker_build['status'] != 200:
			print(docker_build['message'])
			print(docker_build['errcode'])
			return {'status': 400, 'message': docker_build['message']}

		docker_run = Docker.exec('docker run', '-it', '--rm', '-v', '{}:/libsecp/compiled'.format(compiledpath), '--name', 'libsecp-builder-instance')
		if docker_run['status'] != 200:
			print(docker_run['message'])
			print(docker_run['errcode'])
			return {'status': 400, 'message': docker_run['message']}

	def load_library(self) -> dict:
		if sys.platform in ('windows', 'win32') and platform.architecture()[0] == '32bit':
			library_paths = (self.win32bit(), 'libsecp256k1-0.dll')
		elif sys.platform in ('windows', 'win32') and platform.architecture()[0] == '64bit':
			library_paths = (self.win64bit(), 'libsecp256k1-0.dll')
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
			return {'status': 400,
				'message': 'Error: libsecp256k1 library load failed, '.format(repr(exceptions)),
				'data': None}
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
				return {'status': 400,
					'message': 'Error: Invalid libsecp256k1, missing required modules (--enable-module-recovery)',
					'data': None}

			secp256k1.ctx = secp256k1.secp256k1_context_create(SECP256K1_CONTEXT_SIGN | SECP256K1_CONTEXT_VERIFY)
			ret = secp256k1.secp256k1_context_randomize(secp256k1.ctx, os.urandom(32))
			if ret:
				return {'status': 200, 'message': 'Load libsecp256k1 complete.', 'data': secp256k1}
			else:
				return {'status': 400, 'message': 'Error: secp256k1_context_randomize failed', 'data': secp256k1}
		except (OSError, AttributeError) as e:
			return {'status': 400,
				'message': 'Error: Failed to use libsecp256k1, {}'.format(repr(e)), 'data': None}