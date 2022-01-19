#!/usr/bin/python3 -B
from libsecp256k1 import *

def test_main():
	starterpkg = StarterPkg()
	starterpkg.run()

if __name__ == '__main__':
	raise SystemExit(test_main())