#!/bin/bash
set -e
apt-get update
apt-get install -y git automake libtool gcc
apt-get install -y gcc-mingw-w64-i686 gcc-mingw-w64-x86-64
apt-get install -y python3 python3-pip
