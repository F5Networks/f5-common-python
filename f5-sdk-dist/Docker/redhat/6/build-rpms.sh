#!/bin/bash -ex

SRC_DIR=$1
PKG_NAME=f5-sdk
DIST_DIR="${PKG_NAME}-dist"
RPMBUILD_DIR="rpmbuild"
OS_VERSION=6

DEST_DIR="${SRC_DIR}/${DIST_DIR}"

echo "Building ${PKG_NAME} RPM packages..."
buildroot=$(mktemp -d /tmp/${PKG_NAME}.XXXXX)

cp -R $SRC_DIR/* ${buildroot}

pushd ${buildroot}
python setup.py build bdist_rpm --rpm-base rpmbuild

echo "%_topdir ${buildroot}/rpmbuild" > ~/.rpmmacros

python setup.py bdist_rpm --spec-only --dist-dir rpmbuild/SPECS

rpmbuild -ba rpmbuild/SPECS/${PKG_NAME}.spec

mkdir -p ${DEST_DIR}/rpms/build

for pkg in $(ls rpmbuild/RPMS/noarch/*.rpm); do
  if [[ $pkg =~ ".noarch." ]]; then
    mv $pkg ${pkg%%.noarch.rpm}.el${OS_VERSION}.noarch.rpm
  fi
done
cp -R rpmbuild/RPMS/noarch/*.rpm ${DEST_DIR}/rpms/build

popd

rm -rf ${buildroot}

