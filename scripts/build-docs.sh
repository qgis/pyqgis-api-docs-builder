#!/usr/bin/env bash

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd ${DIR}/..

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
      PACKAGE="--package $OPTARG"
    else
      PACKAGE="$PACKAGE $OPTARG"
    fi
    ;;
  c)
    if [[ -z $CLASS ]]; then
      CLASS="--class $OPTARG"
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
shift $(expr $OPTIND - 1)

echo "QGIS VERSION: ${QGIS_VERSION}"
echo "PACKAGE LIMIT: ${PACKAGE}"
echo "SINGLE CLASS: ${CLASS}"

if [[ -n ${QGIS_BUILD_DIR} ]]; then
  export PYTHONPATH=${PYTHONPATH}:$QGIS_BUILD_DIR/output/python
  #export PATH=$PATH:/usr/local/bin/:$QGIS_BUILD_DIR/build/output/bin
fi
export PYTHONPATH=${PYTHONPATH}:${DIR}/..
echo "setting PYTHONPATH ${PYTHONPATH}"

echo "##[group]make API RST ./scripts/make_api_rst.py ${PACKAGE} ${CLASS} -v ${QGIS_VERSION}"

# see https://bugs.launchpad.net/ubuntu/+source/opencv/+bug/1890170?comments=all
export LD_PRELOAD=/lib/x86_64-linux-gnu/libstdc++.so.6

./scripts/make_api_rst.py ${PACKAGE} ${CLASS} -v ${QGIS_VERSION}
cp -r _templates api/${QGIS_VERSION}/_templates
cp -r _static api/${QGIS_VERSION}/_static
echo "##[endgroup]"

echo "##[group]Build HTML"
make prepare QGISVERSION=${QGIS_VERSION}
make html QGISVERSION=${QGIS_VERSION}
echo "##[endgroup]"

popd
