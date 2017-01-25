#!/bin/bash -ex

OS_TYPE=$1

# We should have a least an argument $1...
if [ ${OS_TYPE} == "--help" ] || [ ${OS_TYPE} == "-h" ] || \
        [ "${OS_TYPE}" == "" ] || [ "$2" == "" ] || [ "$3" == "" ]; then
    echo "Standard Usage:
    $0 <os type> <os version> <./path/to/package>
Debug Usage:
    $0 <os type> <os version> <./path/to/package> --debug
Optional --debug operation:
    The results from the test python script will pipe into:
        /tmp/test_install.o"
    exit 1
fi

OS_VERSION=$2
PKG_FULLNAME=$3
if [ '--debug' == "$4" ]; then
    DEBUG=1
else
    DEBUG=0
fi
PKG_NAME="f5-sdk"
DIST_DIR="${PKG_NAME}-dist"

BUILD_CONTAINER="${OS_TYPE}${OS_VERSION}-${PKG_NAME}-pkg-tester"
WORKING_DIR="/var/wdir"

if [[ ${OS_TYPE} == "redhat" ]]; then
	CONTAINER_TYPE="centos${OS_VERSION}"
elif [[ ${OS_TYPE} == "ubuntu" ]]; then
	if [[ ${OS_VERSION} == "14.04" ]]; then
		CONTAINER_TYPE="trusty"
	else
		echo "Only Trusty release currently supported"
		exit 1
	fi
else
	echo "Unsupported target OS (${OS_TYPE})"
	exit 1
fi

DOCKER_DIR="${DIST_DIR}/Docker/${OS_TYPE}/install_test"
DOCKER_FILE="${DOCKER_DIR}/Dockerfile.${CONTAINER_TYPE}"

docker build -t ${BUILD_CONTAINER} -f ${DOCKER_FILE} ${DOCKER_DIR}
if [ ${DEBUG} == 0 ]; then
   docker run --privileged --rm -v $(pwd):${WORKING_DIR} ${BUILD_CONTAINER} \
        ${PKG_FULLNAME}
else
   docker run --privileged --rm -v $(pwd):${WORKING_DIR} ${BUILD_CONTAINER} \
        ${PKG_FULLNAME} > /tmp/test_instal.o
fi
# NOTE: contrary to documentation, the '-d' flag is not required, and
# ${PKG_FULLNAME} is passed.

exit $?
