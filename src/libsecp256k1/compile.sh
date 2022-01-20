#!/bin/bash

set -e

wd=`pwd`

DLL_TARGET_DIR="$wd/compiled/unix" ./make_libsecp265k1.sh

GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="i686-w64-mingw32" DLL_TARGET_DIR="$wd/compiled/win32" ./make_libsecp265k1.sh

GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="x86_64-w64-mingw32" DLL_TARGET_DIR="$wd/compiled/win64" ./make_libsecp265k1.sh

echo Compile complete.
