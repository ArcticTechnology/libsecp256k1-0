#!/bin/bash

set -e

wd=`pwd`

DLL_WORKING_DIR="$wd" DLL_TARGET_DIR="$wd/compiled/unix" ./docker/make_libsecp256k1.sh

DLL_WORKING_DIR="$wd" DLL_TARGET_DIR="$wd/compiled/win32bit" GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="i686-w64-mingw32" ./docker/make_libsecp256k1.sh

DLL_WORKING_DIR="$wd" DLL_TARGET_DIR="$wd/compiled/win64bit" GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="x86_64-w64-mingw32" ./docker/make_libsecp256k1.sh
