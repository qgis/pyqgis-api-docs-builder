from pathlib import Path

from qgis.core import Qgis
from qgis.gui import QgsCodeEditorShell

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorShell(language=Qgis.ScriptLanguage.Bash)
    widget.setText("""#!/bin/bash
[ $# -ne 2 ] && { echo "Usage:"; exit 1; }
[ ! -d "$1" ] && { echo "Error"; exit 1; }
echo "Files with extension .$2 in $1:"
for file in "$1"/*."$2"; do
  size=$(stat -c %s "$file")
  echo "$(basename "$file"): $((size / 1024)) KB"
done""")
    widget.setCursorPosition(1, 10)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorshellbash.png").as_posix())

    widget = QgsCodeEditorShell(language=Qgis.ScriptLanguage.Batch)
    widget.setText("""@echo off
REM This script takes two arguments
if "%~2" == "" (
  echo Usage: %0 directory file_extension
  exit /b 1
)
if not exist %1 (
  echo Error: %1 does not exist or is not a directory.
  exit /b 1
)""")
    widget.setCursorPosition(2, 7)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorshellbatch.png").as_posix())

    return {
        "codeeditorshellbash.png": "QgsCodeEditorShell containing a sample bash shell script",
        "codeeditorshellbatch.png": "QgsCodeEditorShell containing a sample batch script",
    }
