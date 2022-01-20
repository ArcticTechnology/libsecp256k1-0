#!/usr/bin/env bash

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
