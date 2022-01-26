#!/usr/bin/python3 -B
from .libsecp256k1 import Libsecp265k1

def main():
	Libsecp265k1.docker_compile(interactive=True)

if __name__ == '__main__':
	raise SystemExit(main())