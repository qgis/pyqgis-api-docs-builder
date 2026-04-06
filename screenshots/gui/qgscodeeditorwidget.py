from pathlib import Path

from qgis.gui import QgsCodeEditorPython, QgsCodeEditorWidget

from screenshots.utils import ScreenshotUtils


def __generate_screenshots(dest_path: Path):
    editor = QgsCodeEditorPython()
    editor.setText("""def simple_function(x,y,z):
    return [1, 1.2, "val", 'a string', {'a': True, 'b': False}]

@my_decorator
def somefunc(param1: str='', param2=0):
    if param1 > param2: # interesting
        print('Gre\'ater'.lower())
    return (param2 - param1 + 1 + 0b10) or None
""")
    editor.setCursorPosition(1, 4)
    widget = QgsCodeEditorWidget(editor)

    im = ScreenshotUtils.capture_widget(widget, width=490, height=320)
    im.save((dest_path / "codeeditorwidget.png").as_posix())

    widget.showSearchBar()

    im = ScreenshotUtils.capture_widget(widget, width=490, height=400)
    im.save((dest_path / "codeeditorwidgetwithsearch.png").as_posix())

    return {
        "codeeditorwidget.png": "QgsCodeEditorWidget containing a QgsCodeEditorPython editor",
        "codeeditorwidgetwithsearch.png": "QgsCodeEditorWidget showing the search bar",
    }
