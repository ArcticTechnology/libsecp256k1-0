#!/usr/bin/python3 -B
import sys
from libsecp256k1 import *

def test_main():

	_libsecp256k1 = None
	libsecp256k1 = Libsecp265k1()
	try:
		_libsecp256k1 = libsecp256k1.load_library()
		#print(libsecp256k1.win32())
	except BaseException as e:
		print(repr(e))

	if _libsecp256k1 is None:
		# hard fail:
		sys.exit(f"Error: Failed to load libsecp256k1.")

if __name__ == '__main__':
	raise SystemExit(test_main())