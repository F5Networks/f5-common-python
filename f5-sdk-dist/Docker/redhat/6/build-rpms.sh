#!/bin/bash -ex

if [ $# -eq 1 ]; then
    SRC_DIR=$1
elif [ $# -eq 0 ]; then
    SCRIPTNAME="`readlink --canonicalize $0`"
    SRC_DIR="`dirname "$SCRIPTNAME"`/../../../.."
    SRC_DIR="`readlink --canonicalize $SRC_DIR`"
else
    echo "Error: Cound not deduce SRC_DIR, exiting" >&2
fi

PKG_NAME=f5-sdk
DIST_DIR="${PKG_NAME}-dist"
RPMBUILD_DIR="rpmbuild"
DEST_DIR="${SRC_DIR}/${DIST_DIR}"

# Deduce the DIST name from "rpm --showrc"
getdist() {
    rpm --showrc | while read arg1 arg2 arg3; do
	case $arg1 in
	    -[1-9]*:)
		#echo found valid arg1: arg2: $arg2, arg3: $arg3
		case $arg2 in
		    dist)
			#echo found valid arg: arg3: $arg3
			#echo DIST=$arg3
			    echo $arg3
			    ;;
		esac
	esac
    done
}
DIST="`getdist`"
DISTDIR="`echo $DIST | tr -d '.'`"

echo "Building ${PKG_NAME} RPM packages..."
buildroot=$(mktemp -d /tmp/${PKG_NAME}.XXXXX)

cp -R $SRC_DIR/* ${buildroot}

pushd ${buildroot}
python setup.py build bdist_rpm --rpm-base rpmbuild --release=1$DIST

echo "%_topdir ${buildroot}/rpmbuild" > ~/.rpmmacros

python setup.py bdist_rpm --spec-only --dist-dir rpmbuild/SPECS --release=1$DIST

rpmbuild -ba rpmbuild/SPECS/${PKG_NAME}.spec

# Use DIST specific subdirectories
install -D rpmbuild/RPMS/*/*.rpm "${DEST_DIR}/rpms/build/$DISTDIR/RPMS/"
install -D rpmbuild/SRPMS/*.rpm "${DEST_DIR}/rpms/build/$DISTDIR/SRPMS/"

popd

#rm -rf ${buildroot}

