#!/bin/bash

set -e

wd=`pwd`

DLL_TARGET_DIR="$wd/compiled/unix" ./make_libsecp256k1.sh

DLL_TARGET_DIR="$wd/compiled/win32bit" GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="i686-w64-mingw32" ./make_libsecp256k1.sh

DLL_TARGET_DIR="$wd/compiled/win64bit" GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="x86_64-w64-mingw32" ./make_libsecp256k1.sh
