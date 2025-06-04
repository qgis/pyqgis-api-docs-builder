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

#### Debugging with VS Code

Run the build with option `-d`:

```bash
./scripts/run-docker.sh -d
```

or:

```bash
./scripts/build-docs.sh -d
```

When the output stops on:

```
0.00s - Debugger warning: It seems that frozen modules are being used, which may
0.00s - make the debugger miss breakpoints. Please pass -Xfrozen_modules=off
0.00s - to python to disable frozen modules.
0.00s - Note: Debugging will proceed. Set PYDEVD_DISABLE_FILE_VALIDATION=1 to disable this validation.
```

You should attach your VS Code debugger on local port 5678.

Here is an example `.vscode/launch.json` file for the Docker run:

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Remote Attach",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app/pyqgis"
                }
            ]
        }
    ]
}
```

## Viewing the docs

Open the build/html/ contents in your web browser.

## Credits

- Tim Sutton 2017 - Initial prototype for this build system
- Denis Rouzaud 2017 - Including work funded by QGIS.org
