#!/bin/bash

set -e

. $(dirname "$0")/helper.sh || (echo "Could not source helper.sh" && exit 1)

wd=`pwd`

DLL_TARGET_DIR="$wd/compiled/unix" ./make_libsecp265k1.sh

GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="i686-w64-mingw32" DLL_TARGET_DIR="$wd/compiled/win32" ./make_libsecp265k1.sh

GCC_STRIP_BINARIES="1" GCC_TRIPLET_HOST="x86_64-w64-mingw32" DLL_TARGET_DIR="$wd/compiled/win64" ./make_libsecp265k1.sh

echo Compile complete.
