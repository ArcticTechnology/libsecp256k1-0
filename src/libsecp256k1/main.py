#!/usr/bin/python3 -B
from .libsecp256k1 import Libsecp265k1

def main():
	libsecp256k1 = Libsecp265k1()
	libsecp256k1.docker_compile()

if __name__ == '__main__':
	raise SystemExit(main())