#!/usr/bin/env bash

set -e

IFS=', ' read -r -a VERSIONS <<< "$1"
echo "versions: ${VERSIONS}"

# GNU prefix command for mac os support (gsed, gsplit)
GP=
if [[ "$OSTYPE" =~ darwin* ]]; then
  GP=g
fi

echo "Current dir: $(pwd)"


echo "*** Create publish directory"
mkdir -p "publish"
rm -rf publish/*
pushd publish

echo "*** Clone gh-pages branch"
OUTPUT=${QGIS_VERSION}
if [[ -n ${GITHUB_RUN_ID} ]]; then
  git config --global user.email "qgisninja@gmail.com"
  git config --global user.name "Geo-Ninja"
  git clone https://${GH_TOKEN}@github.com/qgis/pyqgis.git --depth 100 --branch gh-pages
  pushd pyqgis
  # merge commit to lower repo size
  git reset --hard HEAD~99
  git merge --squash HEAD@{1}
  git commit -m "Update docs"
else
  git clone git@github.com:qgis/pyqgis.git --depth 1 --branch gh-pages
  pushd pyqgis
fi

if [[ -n ${FIX_VERSION} ]]; then
  echo "fixing versions...."
  IFS=', ' read -r -a ALL_VERSIONS <<< $(${GP}sed -n 's/version_list: //p' ../../pyqgis_conf.yml)
  HTML=""
  for v in "${ALL_VERSIONS[@]}"; do
    HTML="${HTML}\n      \n        <dd><a href=\"https://qgis.org/pyqgis/${v}\">${v}</a></dd>"
  done
  export LANGUAGE=en_US.UTF-8
  export LANG=en_US.UTF-8
  export LC_ALL=en_US.UTF-8
  find . -type f -iname "*.html" -exec perl -i -p0e "s@<dl>(\s*)<dt>Versions</dt>.*</dl>@<dl>\1<dt>Versions</dt>${HTML}\n      \n    </dl>@smg" {} \;
else
  for VERSION in "${VERSIONS[@]}"; do
    echo "get ${VERSION}"
    rm -rf ${VERSION}
    mkdir "${VERSION}"
    cp -R ../../${VERSION}/html/* ${VERSION}/
  done
fi

echo "##[group] Git commit"
echo "*** Add and push"
git add --all
git commit -m "Update docs"
echo "##[endgroup]"
if [[ -n ${GITHUB_RUN_ID} ]]; then
  echo "pushing from CI without confirmation"
  git push -f
else
  read -p "Are you sure to push? (y/n)" -n 1 -r response
  echo    # (optional) move to a new line
  if [[ $response =~ ^[Yy](es)?$ ]]; then
      git push
  fi
fi
popd
popd
