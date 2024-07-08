[![Read the documentation](https://img.shields.io/badge/Read-the%20docs-green.svg)](https://qgis.org/pyqgis/master/index.html)

# QGIS Python API Documentation

This a Sphinx project to build python API documentation for QGIS.
It does not contain the actual documentation itself which is hold in QGIS source code at https://github.com/qgis/QGIS/.

You can see an online version of the generated documentation at this
website:

https://qgis.org/pyqgis/master/index.html

## Building the docs

### With official Docker images

You can build the documentation for a specific QGIS versions by calling

```./scripts/run-docker.sh -v 3.40```

### From your own QGIS build

Call ``build-docs.sh``. QGIS python package must be found.
You can either:

* export the PYTHONPATH yourself
* export your QGIS build directory with ``export QGIS_BUILD_DIR=~/dev/QGIS/build``
* or provide QGIS build directory as argument to the script: ``./build-docs.sh -qgis-build-dir ~/dev/QGIS/build``

### Testing & development

For testing and development, you can restrict the build of the documentation to specific classes to get faster builds:

For a quick local run on a specific version (few classes):
```./scripts/run-docker.sh -v 3.40 -c QgsVectorLayer -c QgsFeature```

For all core (but no gui, analysis, etc):
```./scripts/run-docker.sh -p core```

## Viewing the docs

Open the build/html/ contents in your web browser.

## Publishing the docs

Use the ``publish-docs.sh`` script, with having build the docs before publishing them.

## Credits

- Tim Sutton 2017 - Initial prototype for this build system
- Denis Rouzaud 2017 - Including work funded by QGIS.org
