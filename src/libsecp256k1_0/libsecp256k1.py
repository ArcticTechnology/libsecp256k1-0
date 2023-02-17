# Libsecp256k1-0
# Copyright (c) 2022 Arctic Technology

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

class Libsecp256k1:

	@classmethod
	def get_lib_path(self, filepath: str) -> str:
		return Crawler.joinpath(os.path.dirname(__file__), filepath)

	@classmethod
	def unix(self) -> str:
		return self.get_lib_path('compiled/unix/libsecp256k1.so.0')

	@classmethod
	def win32bit(self) -> str:
		return self.get_lib_path('compiled/win32bit/libsecp256k1-0.dll')

	@classmethod
	def win64bit(self) -> str:
		return self.get_lib_path('compiled/win64bit/libsecp256k1-0.dll')

	@classmethod
	def darwin(self) -> str:
		return self.get_lib_path('compiled/darwin/libsecp256k1.0.dylib')

	@classmethod
	def docker_compile(self, outpath: str = None, interactive: bool = False, sudo: bool = False) -> dict:
		dockerhome = '/home/ubuntu/libsecp256k1'
		dockercompiled = Crawler.joinpath(dockerhome, 'compiled')
		if sudo == True:
			prefix = 'sudo '
		else:
			prefix = ''

		if outpath == None:
			mountpath = self.get_lib_path('compiled')
		else:
			if isdir(outpath) == False:
				message = 'Error: Invalid output path, no action taken.'; print(message)
				return {'status': 400, 'message': message}
			else:
				mountpath = Crawler.joinpath(outpath, 'compiled')

		if interactive == True and isdir(mountpath):
			print(' ')
			print('Existing output path found: {}'.format(mountpath))
			print(' ')
			print('Would you like to overwrite this? [y/n]')
			select = input()
			os.system('clear')
			if select != 'y':
				message = 'Exited, no action taken.'; print(message)
				return {'status': 400, 'message': message}

		print('Building docker environment.....')
		dockerpath = self.get_lib_path('docker')
		docker_build = Docker.exec('{}docker build'.format(prefix), '-t', 'libsecp-builder', dockerpath)
		if docker_build['status'] != 200:
			print(docker_build['message'])
			print(docker_build['errcode'])
			return {'status': 400, 'message': docker_build['message']}

		print('Compiling libsecp256k1 with docker.....')
		docker_run = Docker.exec('{}docker run'.format(prefix), '-it', '--rm', '-v', '{m}:{d}'.format(m=mountpath,d=dockercompiled),
								'--name', 'libsecp-builder-instance', 'libsecp-builder')
		if docker_run['status'] != 200:
			print(docker_run['message'])
			print(docker_run['errcode'])
			return {'status': 400, 'message': docker_run['message']}
		else:
			print('Copied {d} to {m}'.format(d=dockercompiled,m=mountpath))
			print('Successfully compiled libsecp256k1.')
			print(' ')
			return {'status': 200, 'message': docker_run['message']}

	@classmethod
	def load_library(self) -> dict:
		if sys.platform in ('windows', 'win32') and platform.architecture()[0] == '32bit':
			library_paths = (self.win32bit(), 'libsecp256k1-0.dll')
		elif sys.platform in ('windows', 'win32') and platform.architecture()[0] == '64bit':
			library_paths = (self.win64bit(), 'libsecp256k1-0.dll')
		elif sys.platform in ('darwin'):
			library_paths = (self.darwin(), 'libsecp256k1.0.dylib')
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
				'message': 'Error: Failed to load libsecp256k1 library. {}'.format(repr(exceptions)),
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
				return {'status': 400, 'message': 'Error: Failed to secure libsecp256k1.', 'data': secp256k1}
		except (OSError, AttributeError) as e:
			return {'status': 400,
				'message': 'Error: Failed to use libsecp256k1. {}'.format(repr(e)), 'data': None}

class Secp256k1:

	_load = Libsecp256k1.load_library()
	if _load['status'] == 200:
		_libsecp256k1 = _load['data']
	else:
		_libsecp256k1 = None
		sys.exit(_load['message'])
