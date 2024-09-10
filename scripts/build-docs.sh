#!/usr/bin/env bash

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

GP=
if [[ "$OSTYPE" == *bsd* ]] || [[ "$OSTYPE" =~ darwin* ]]; then
  GP=g
fi

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
shift $((OPTIND-1))

if [[ ${QGIS_VERSION} == 'master' ]]; then
  RELEASE_TAG=${QGIS_VERSION}
else
  RELEASE_TAG="release-${QGIS_VERSION//./_}"

  echo $(apt list --installed qgis)

  VERSION_INSTALLED=$(apt list --installed qgis | grep installed | cut -d: -f2 | cut -d\+ -f1)
  if [[ ${VERSION_INSTALLED} =~ ^${QGIS_VERSION}\.[0-9]+$ ]]; then
    echo "version check ok: ${VERSION_INSTALLED}"
  else
    echo "Version checked failed!"
    echo "version installed: ${VERSION_INSTALLED}"
    echo "version to build: ${QGIS_VERSION}"
    exit 1
  fi
fi

echo "QGIS VERSION: ${QGIS_VERSION}"
echo "RELEASE TAG: ${RELEASE_TAG}"
echo "PACKAGE LIMIT: ${PACKAGE}"
echo "SINGLE CLASS: ${CLASS}"

# download class_map until correctly installed
# TODO: remove this when https://github.com/qgis/QGIS/pull/58200 is merged
for module in "3d" "analysis" "core" "gui" "server"; do
    wget -O /usr/lib/python3/dist-packages/qgis/${module}/class_map.yaml https://raw.githubusercontent.com/qgis/QGIS/${RELEASE_TAG}/python/${module}/class_map.yaml
done

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
${GP}sed -r "s/__QGIS_VERSION__/${QGIS_VERSION}/g;" conf.in.py > api/${QGIS_VERSION}/conf.py
sphinx-build -M html api/${QGIS_VERSION} build/${QGIS_VERSION} -T -j auto
echo "##[endgroup]"

echo "##[group]Move files around"
rm -rf build/${QGIS_VERSION}/doctrees
mv build/${QGIS_VERSION}/html/* build/${QGIS_VERSION}
rm -rf build/${QGIS_VERSION}/html
echo "##[endgroup]"

popd
