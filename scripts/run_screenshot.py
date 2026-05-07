#!/usr/bin/env python3
"""
Runs a single screenshot script in an isolated process.

Usage: run_screenshot.py <script_path> <output_path>

Initializes a QgsApplication, executes the screenshot script's
__generate_screenshots function, and prints the resulting image
mapping as JSON to stdout.
"""

import importlib.util
import json
import os
import sys
from pathlib import Path

# ensure the project root is importable (for screenshots.utils etc.)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from qgis._3d import Qgs3D  # noqa: E402
from qgis.core import QgsApplication, QgsSettings  # noqa: E402
from qgis.PyQt.QtCore import QCoreApplication  # noqa: E402
from qgis.PyQt.QtGui import QFont  # noqa: E402

QCoreApplication.setOrganizationName("QGIS_PyQGISApiDocsBuilder")
QCoreApplication.setOrganizationDomain("PyQGISApiDocsBuilder.com")
QCoreApplication.setApplicationName("PyQGISApiDocsBuilder")
QgsSettings().clear()

qgs = QgsApplication([], False)
qgs.initQgis()
font = QFont("Noto Sans")
font.setPointSize(10)
qgs.setFont(font)

Qgs3D.initialize()

script_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])

spec = importlib.util.spec_from_file_location("script", script_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

images = mod.__generate_screenshots(output_path)
print(json.dumps(images), flush=True)

# Some widgets (e.g. those embedding QgsMapCanvas) leave Qt rendering threads
# alive at exit, which causes SIGSEGV during Python interpreter shutdown.
# Skip regular cleanup since we already have the result.
os._exit(0)
