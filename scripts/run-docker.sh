#!/usr/bin/env bash

# for a quick local run (few classes):
# QGIS_VERSION_BRANCH=master BUILD_OPTIONS='-c QgsVectorLayer -c QgsFeature' PUBLISH=false ./scripts/run-docker.sh
# or for all core (but no gui, analysis, etc):
# QGIS_VERSION_BRANCH=master BUILD_OPTIONS='-p core' PUBLISH=false ./scripts/run-docker.sh

set -e

# GNU prefix command for mac os support (gsed, gsplit)
GP=
if [[ "$OSTYPE" =~ darwin* ]]; then
  GP=g
fi

DIR=$(git rev-parse --show-toplevel)

pushd ${DIR}

QGIS_DOCKER_TAG="${QGIS_VERSION//master/latest}"

echo "QGIS Docker tag: ${QGIS_DOCKER_TAG}"
echo "Building for QGIS: ${QGIS_VERSION}"

echo "##[group] Pull QGIS"96+3
docker pull "qgis/qgis:${QGIS_DOCKER_TAG}"
echo "##[endgroup]"

echo "##[group] Docker build"
docker build --build-arg QGIS_DOCKER_TAG=${QGIS_DOCKER_TAG} -t qgis/qgis-python-api-doc:${QGIS_DOCKER_TAG} .
echo "##[endgroup]"

echo "##[group] Docker run"
docker rm -f pyqgis || true
docker run --name pyqgis \
  -e "QGIS_VERSION=${QGIS_VERSION}" \
  -e "BUILD_OPTIONS=${BUILD_OPTIONS}" \
  qgis/qgis-python-api-doc:${QGIS_DOCKER_TAG}
echo "##[endgroup]"

echo "Copy files"
mkdir -p ${DIR}/build
mkdir -p ${DIR}/build/${QGIS_VERSION}
CONTAINER_ID=$(docker ps -aqf "name=pyqgis")
docker cp ${CONTAINER_ID}:/root/pyqgis/build/${QGIS_VERSION}/html ${DIR}/build/${QGIS_VERSION}

popd
