#!/bin/bash

# The following is a modified version of make_libsecp256k1.sh from
# https://github.com/spesmilo/electrum/blob/master/contrib/make_libsecp256k1.sh
# which is subject to the following license.
#
# Copyright (C) 2011 thomasv@gitorious
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

LIBSECP_VERSION="dbd41db16a0e91b2566820898a3ab2d7dad4fe00"

function clone_repo() {
	git clone https://github.com/bitcoin-core/secp256k1.git
}

set -e

. $(dirname "$0")/helper.sh || (echo "Could not source helper.sh" && exit 1)

if [ -n "$DLL_WORKING_DIR" ] ; then
	wd="$DLL_WORKING_DIR"
else
	wd=`pwd`
fi

COMPILED="$wd/compiled"
BUILD="$COMPILED/build"
DIST="$COMPILED/dist"

pkgname="secp256k1"
info "Building $pkgname..."

(
	mkdir -p $BUILD
	cd $BUILD
	if [ ! -d secp256k1 ]; then
		clone_repo
	fi
	cd secp256k1
	if ! $(git cat-file -e ${LIBSECP_VERSION}) ; then
		info "Could not find requested version $LIBSECP_VERSION in local clone; fetching..."
		git fetch --all
	fi
	git reset --hard
	git clean -dfxq
	git checkout "${LIBSECP_VERSION}^{commit}"

	if ! [ -x configure ] ; then
		echo "libsecp256k1_la_LDFLAGS = -no-undefined" >> Makefile.am
		echo "LDFLAGS = -no-undefined" >> Makefile.am
		./autogen.sh || fail "Could not run autogen for $pkgname. Please make sure you have automake and libtool installed, and try again."
	fi
	if ! [ -r config.status ] ; then
		./configure \
			$AUTOCONF_FLAGS \
			--prefix="$DIST/$pkgname" \
			--enable-module-recovery \
			--enable-experimental \
			--enable-module-ecdh \
			--disable-benchmark \
			--disable-tests \
			--disable-exhaustive-tests \
			--disable-static \
			--enable-shared || fail "Could not configure $pkgname. Please make sure you have a C compiler installed and try again."
	fi
	make -j4 || fail "Could not build $pkgname"
	make install || fail "Could not install $pkgname"
	. "$DIST/$pkgname/lib/libsecp256k1.la"
	host_strip "$DIST/$pkgname/lib/$dlname"

	if [ -n "$DLL_TARGET_DIR" ] ; then
		mkdir -p $DLL_TARGET_DIR
		cp -fpv "$DIST/$pkgname/lib/$dlname" "$DLL_TARGET_DIR" || fail "Could not copy the $pkgname binary to $DLL_TARGET_DIR"
		info "$dlname has been created in $DLL_TARGET_DIR"
	else
		cp -fpv "$DIST/$pkgname/lib/$dlname" "$DIST" || fail "Could not copy the $pkgname binary to its destination"
		info "$dlname has been created in $DIST"
	fi
)