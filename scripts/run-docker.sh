#!/usr/bin/env bash

# for a quick local run on a specific version (few classes):
# ./scripts/run-docker.sh -v 3.40 -c QgsVectorLayer -c QgsFeature
# or for all core (but no gui, analysis, etc):
# ./scripts/run-docker.sh -p core

set -e

QGIS_VERSION=master
while getopts "q:p:c:v:" opt; do
  case $opt in
  v)
    QGIS_VERSION=$OPTARG
    ;;
  q)
    QGIS_BUILD_DIR=$OPTARG
    ;;
  p)
    if [[ -z $PACKAGE ]]; then
      PACKAGE="-p $OPTARG"
    else
      PACKAGE="$PACKAGE $OPTARG"
    fi
    ;;
  c)
    if [[ -z $CLASS ]]; then
      CLASS="-c $OPTARG"
    else
      CLASS="$CLASS $OPTARG"
    fi
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    exit 1
    ;;
  esac
done
shift $((OPTIND-1))

# GNU prefix command for mac os support (gsed, gsplit)
GP=
if [[ "$OSTYPE" =~ darwin* ]]; then
  GP=g
fi

DIR=$(git rev-parse --show-toplevel)


QGIS_DOCKER_TAG="${QGIS_VERSION//master/latest}"

echo "QGIS Docker tag: ${QGIS_DOCKER_TAG}"
echo "Building for QGIS: ${QGIS_VERSION}"

echo "##[group] Pull QGIS"
docker pull "qgis/qgis:${QGIS_DOCKER_TAG}"
echo "##[endgroup]"

echo "##[group] Docker build"
docker build --build-arg QGIS_DOCKER_TAG=${QGIS_DOCKER_TAG} -t qgis/qgis-python-api-doc:${QGIS_DOCKER_TAG} ${DIR}
echo "##[endgroup]"

echo "##[group] Docker run"
docker rm -f pyqgis || true
docker run -v ${DIR}:/root/pyqgis \
  qgis/qgis-python-api-doc:${QGIS_DOCKER_TAG} \
  /bin/bash -c "/root/pyqgis/scripts/build-docs.sh ${PACKAGE} ${CLASS} -v ${QGIS_VERSION}"
echo "##[endgroup]"
