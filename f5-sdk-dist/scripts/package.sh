#!/bin/bash -ex

OS_TYPE=$1
OS_VERSION=$2
PKG_NAME="f5-sdk"
DIST_DIR="${PKG_NAME}-dist"

BUILD_CONTAINER=${OS_TYPE}${OS_VERSION}-${PKG_NAME}-builder
WORKING_DIR="/var/wdir"

if [[ ${OS_TYPE} == "redhat" ]]; then
	PKG_TYPE="rpms"
elif [[ ${OS_TYPE} == "ubuntu" ]]; then
	PKG_TYPE="debs"
else
	echo "Unsupported target OS (${OS_TYPE})"
	exit 1
fi

docker build -t ${BUILD_CONTAINER} ${DIST_DIR}/Docker/${OS_TYPE}/${OS_VERSION}
docker run --privileged --rm -v $(pwd):${WORKING_DIR} ${BUILD_CONTAINER} /bin/bash /build-${PKG_TYPE}.sh "${WORKING_DIR}"
sudo chown -R travis:travis ${DIST_DIR}

exit 0
