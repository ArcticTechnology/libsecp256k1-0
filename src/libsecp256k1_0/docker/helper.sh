#!/usr/bin/env bash

# Libsecp256k1-0
# Copyright (c) 2023 Arctic Technology

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

umask 0022

RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

function info {
	printf "\r ${BLUE}INFO:${NC} ${1}\n"
}

function fail {
	printf "\r ${RED}ERROR:${NC} ${1}\n"
	exit 1
}

function warn {
	printf "\r ${YELLOW}WARNING:${NC} ${1}\n"
}

function gcc_with_triplet() {
	TRIPLET="$1"
	CMD="$2"
	shift 2
	if [ -n "$TRIPLET" ] ; then
		"$TRIPLET-$CMD" "$@"
	else
		"$CMD" "$@"
	fi
}

function gcc_host() {
	gcc_with_triplet "$GCC_TRIPLET_HOST" "$@"
}

function gcc_build() {
	gcc_with_triplet "$GCC_TRIPLET_BUILD" "$@"
}

function host_strip() {
	if [ "$GCC_STRIP_BINARIES" -ne "0" ] ; then
		case "$BUILD_TYPE" in
			linux|wine)
				gcc_host strip "$@"
				;;
			darwin)
				# Strip needed for macOS?
				;;
		esac
	fi
}

export SOURCE_DATE_EPOCH=1530212462
export ZERO_AR_DATE=1 # for macOS
export PYTHONHASHSEED=22
# Set the build type, overridden by wine build
export BUILD_TYPE="${BUILD_TYPE:-$(uname | tr '[:upper:]' '[:lower:]')}"
# Add host / build flags if the triplets are set
if [ -n "$GCC_TRIPLET_HOST" ] ; then
	export AUTOCONF_FLAGS="$AUTOCONF_FLAGS --host=$GCC_TRIPLET_HOST"
fi
if [ -n "$GCC_TRIPLET_BUILD" ] ; then
	export AUTOCONF_FLAGS="$AUTOCONF_FLAGS --build=$GCC_TRIPLET_BUILD"
fi

export GCC_STRIP_BINARIES="${GCC_STRIP_BINARIES:-0}"
