#!/usr/bin/env bash

set -e

VERSIONS=(master 3.36 3.34 3.32 3.30 3.28 3.26 3.24 3.22 3.20 3.18 3.16 3.14 3.12 3.10 3.8 3.6 3.4 3.2 3.0)
for v in "${VERSIONS[@]}"; do
  HTML="${HTML}\n      \n        <dd><a href=\"https://qgis.org/pyqgis/${v}\">${v}</a></dd>"
done

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

for v in "${VERSIONS[@]}"; do
  echo "fixing $v"
  find ${v} -type f -iname "*.html" -exec perl -i -p0e "s@<dl>(\s*)<dt>Versions</dt>.*</dl>@<dl>\1<dt>Versions</dt>${HTML}\n      \n    </dl>@smg" {} \;
done
