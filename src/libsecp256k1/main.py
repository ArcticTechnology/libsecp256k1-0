#!/usr/bin/python3 -B
from .libsecp256k1 import StarterPkg

def main():
	starterpkg = StarterPkg()
	starterpkg.run()

if __name__ == '__main__':
	raise SystemExit(main())