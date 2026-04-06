from pathlib import Path

from qgis.gui import QgsCodeEditorPython

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    widget = QgsCodeEditorPython()
    widget.setText("""def simple_function(x,y,z):
    return [1, 1.2, "val", 'a string', {'a': True, 'b': False}]

@my_decorator
def somefunc(param1: str='', param2=0):
    if param1 > param2: # interesting
        print('Gre\'ater'.lower())
    return (param2 - param1 + 1 + 0b10) or None
""")
    widget.setCursorPosition(1, 4)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorpython.png").as_posix())

    return {"codeeditorpython.png": "QgsCodeEditorPython containing sample Python"}
