"""
Test documenters
"""

import unittest

from docs_builder.documenters import OverloadedPythonMethodDocumenter


class TestConversionContext(unittest.TestCase):
    """
    Test documenters
    """

    def test_parse_signature_blocks(self):
        """
        Test extracting overrloaded signatures
        """
        # simple single signature
        self.assertEqual(
            OverloadedPythonMethodDocumenter.parse_signature_blocks(
                """instance() -> QgsProject
Returns the QgsProject singleton instance"""
            ),
            [("() -> QgsProject", "Returns the QgsProject singleton instance\n")],
        )

        # simple overloads
        self.assertEqual(
            OverloadedPythonMethodDocumenter.parse_signature_blocks(
                """write(self, filename: Optional[str]) -> bool
Writes the project to a file.

:param filename: destination file

:return: ``True`` if project was written successfully

.. note::

   calling this implicitly sets the project's filename (see :py:func:`~QgsProject.setFileName` )

.. note::

   :py:func:`~QgsProject.isDirty` will be set to ``False`` if project is successfully written

write(self) -> bool
Writes the project to its current associated file (see
:py:func:`~QgsProject.fileName` ).

:return: ``True`` if project was written successfully

.. note::

   :py:func:`~QgsProject.isDirty` will be set to ``False`` if project is successfully written"""
            ),
            [
                (
                    "(self, filename: Optional[str]) -> bool",
                    """Writes the project to a file.

:param filename: destination file

:return: ``True`` if project was written successfully

.. note::

   calling this implicitly sets the project's filename (see :py:func:`~QgsProject.setFileName` )

.. note::

   :py:func:`~QgsProject.isDirty` will be set to ``False`` if project is successfully written

""",
                ),
                (
                    "(self) -> bool",
                    """Writes the project to its current associated file (see
:py:func:`~QgsProject.fileName` ).

:return: ``True`` if project was written successfully

.. note::

   :py:func:`~QgsProject.isDirty` will be set to ``False`` if project is successfully written
""",
                ),
            ],
        )

        # complex overloads
        self.assertEqual(
            OverloadedPythonMethodDocumenter.parse_signature_blocks(
                """getFeatures(self, request: QgsFeatureRequest = QgsFeatureRequest()) -> QgsFeatureIterator
Queries the layer for features specified in request.

:param request: feature request describing parameters of features to
                return

:return: iterator for matching features from provider

getFeatures(self, expression: Optional[str]) -> QgsFeatureIterator
Queries the layer for features matching a given expression.

getFeatures(self, fids: object) -> QgsFeatureIterator
Queries the layer for the features with the given ids.

getFeatures(self, rectangle: QgsRectangle) -> QgsFeatureIterator
Queries the layer for the features which intersect the specified
rectangle."""
            ),
            [
                (
                    "(self, request: QgsFeatureRequest = QgsFeatureRequest()) -> QgsFeatureIterator",
                    """Queries the layer for features specified in request.

:param request: feature request describing parameters of features to
                return

:return: iterator for matching features from provider

""",
                ),
                (
                    "(self, expression: Optional[str]) -> QgsFeatureIterator",
                    """Queries the layer for features matching a given expression.

""",
                ),
                (
                    "(self, fids: object) -> QgsFeatureIterator",
                    """Queries the layer for the features with the given ids.

""",
                ),
                (
                    "(self, rectangle: QgsRectangle) -> QgsFeatureIterator",
                    """Queries the layer for the features which intersect the specified
rectangle.
""",
                ),
            ],
        )

        # complex overload
        self.assertEqual(
            OverloadedPythonMethodDocumenter.parse_signature_blocks(
                """loadNamedStyle(self, theURI: Optional[str], loadFromLocalDb: bool, categories: Union[QgsMapLayer.StyleCategories, QgsMapLayer.StyleCategory] = QgsMapLayer.AllStyleCategories, flags: Union[Qgis.LoadStyleFlags, Qgis.LoadStyleFlag] = Qgis.LoadStyleFlags()) -> Tuple[str, bool]
Loads a named style from file/local db/datasource db

:param theURI: the URI of the style or the URI of the layer
:param loadFromLocalDb: if ``True`` forces to load from local db instead
                        of datasource one
:param categories: the style categories to be loaded.
:param flags: flags controlling how the style should be loaded (since
              QGIS 3.38)

:return: - status message, which may indicate success or contain an
           error message
         - resultFlag: ``True`` if a named style is correctly loaded

loadNamedStyle(self, uri: Optional[str], categories: Union[QgsMapLayer.StyleCategories, QgsMapLayer.StyleCategory] = QgsMapLayer.AllStyleCategories, flags: Union[Qgis.LoadStyleFlags, Qgis.LoadStyleFlag] = Qgis.LoadStyleFlags()) -> Tuple[str, bool]
Retrieve a named style for this layer if one exists (either as a .qml
file on disk or as a record in the users style table in their personal
qgis.db)

:param uri: the file name or other URI for the style file. First an
            attempt will be made to see if this is a file and load that,
            if that fails the qgis.db styles table will be consulted to
            see if there is a style who's key matches the URI.
:param categories: the style categories to be loaded.
:param flags: flags controlling how the style should be loaded (since
              QGIS 3.38)

:return: - a QString with any status messages
         - resultFlag: a reference to a flag that ``False`` if we did
           not manage to load the default style.

.. seealso:: :py:func:`loadDefaultStyle`
"""
            ),
            [
                (
                    "(self, theURI: Optional[str], loadFromLocalDb: bool, categories: Union[QgsMapLayer.StyleCategories, QgsMapLayer.StyleCategory] = QgsMapLayer.AllStyleCategories, flags: Union[Qgis.LoadStyleFlags, Qgis.LoadStyleFlag] = Qgis.LoadStyleFlags()) -> Tuple[str, bool]",
                    """Loads a named style from file/local db/datasource db

:param theURI: the URI of the style or the URI of the layer
:param loadFromLocalDb: if ``True`` forces to load from local db instead
                        of datasource one
:param categories: the style categories to be loaded.
:param flags: flags controlling how the style should be loaded (since
              QGIS 3.38)

:return: - status message, which may indicate success or contain an
           error message
         - resultFlag: ``True`` if a named style is correctly loaded

""",
                ),
                (
                    "(self, uri: Optional[str], categories: Union[QgsMapLayer.StyleCategories, QgsMapLayer.StyleCategory] = QgsMapLayer.AllStyleCategories, flags: Union[Qgis.LoadStyleFlags, Qgis.LoadStyleFlag] = Qgis.LoadStyleFlags()) -> Tuple[str, bool]",
                    """Retrieve a named style for this layer if one exists (either as a .qml
file on disk or as a record in the users style table in their personal
qgis.db)

:param uri: the file name or other URI for the style file. First an
            attempt will be made to see if this is a file and load that,
            if that fails the qgis.db styles table will be consulted to
            see if there is a style who's key matches the URI.
:param categories: the style categories to be loaded.
:param flags: flags controlling how the style should be loaded (since
              QGIS 3.38)

:return: - a QString with any status messages
         - resultFlag: a reference to a flag that ``False`` if we did
           not manage to load the default style.

.. seealso:: :py:func:`loadDefaultStyle`

""",
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
