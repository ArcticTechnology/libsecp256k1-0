#!/usr/bin/python3 -B
from .libsecp256k1 import Libsecp256k1

def main():
	Libsecp256k1.docker_compile(interactive=True, sudo=True)

if __name__ == '__main__':
	raise SystemExit(main())