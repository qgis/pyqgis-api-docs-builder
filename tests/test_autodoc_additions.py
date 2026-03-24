"""
Test autodoc additions
"""

import unittest

from docs_builder.autodoc import AutoDocAdditions


class TestAutoDocAdditions(unittest.TestCase):
    """
    Test autodoc additions
    """

    def test_process_docstring_for_methods(self):
        """
        Test logic for processing the docstrings for methods
        """

        def dummy_method():
            """
            xxx
            """

        lines = [
            "Adds a single ``feature`` to the sink. Feature addition behavior is",
            "controlled by the specified ``flags``.",
            "",
            ".. seealso:: QgsVectorLayer for another class",
            "",
            ".. seealso:: :py:func:`addFeatures`",
            "",
            ":return: ``True`` in case of success and ``False`` in case of failure",
            "",
        ]
        AutoDocAdditions.process_docstring(
            app=None,
            what="method",
            name="qgis.core.QgsFeatureSink.addFeature",
            obj=dummy_method,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Adds a single ``feature`` to the sink. Feature addition behavior is",
                "controlled by the specified ``flags``.",
                "",
                ".. seealso:: :py:class:`.QgsVectorLayer` for another class",
                "",
                ".. seealso:: :py:func:`addFeatures`",
                "",
                ":return: ``True`` in case of success and ``False`` in case of failure",
                "",
            ],
        )

        # with code example
        lines = [
            "Adds a single ``feature`` to the sink. Feature addition behavior is",
            "controlled by the specified ``flags``.",
            "",
            ".. code-block:",
            "",
            "  class MyClass(QgsMapLayer):",
            "    pass" "",
            "",
            ":return: ``True`` in case of success and ``False`` in case of failure",
            "",
        ]
        AutoDocAdditions.process_docstring(
            app=None,
            what="method",
            name="qgis.core.QgsFeatureSink.addFeature",
            obj=dummy_method,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Adds a single ``feature`` to the sink. Feature addition behavior is",
                "controlled by the specified ``flags``.",
                "",
                ".. code-block:",
                "",
                "  class MyClass(QgsMapLayer):",
                "    pass",
                "",
                ":return: ``True`` in case of success and ``False`` in case of failure",
                "",
            ],
        )

        # overloaded method style docstring
        lines = [
            "addRing(self, ring: Iterable[QgsPointXY]) -> Qgis.GeometryOperationResult",
            "Adds a new ring to this geometry. This makes only sense for polygon and",
            "multipolygons.",
            "",
            ":param ring: The ring to be added",
            "",
            ":return: OperationResult a result code: success or reason of failure",
            "",
            "",
        ]
        AutoDocAdditions.process_docstring(
            app=None,
            what="method",
            name="qgis.core.QgsGeometry.addRing",
            obj=dummy_method,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Adds a new ring to this geometry. This makes only sense for polygon and",
                "multipolygons.",
                "",
                ":type ring: Iterable[QgsPointXY]",
                ":param ring: The ring to be added",
                "",
                ":rtype: Qgis.GeometryOperationResult",
                ":return: OperationResult a result code: success or reason of failure",
                "",
                "",
            ],
        )

        lines = [
            "addRing(self, ring: QgsCurve) -> Qgis.GeometryOperationResult",
            "Adds a new ring to this geometry. This makes only sense for polygon and",
            "multipolygons.",
            "",
            ":param ring: The ring to be added",
            "",
            ":return: OperationResult a result code: success or reason of failure",
            "",
        ]

        AutoDocAdditions.process_docstring(
            app=None,
            what="method",
            name="qgis.core.QgsGeometry.addRing",
            obj=dummy_method,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Adds a new ring to this geometry. This makes only sense for polygon and",
                "multipolygons.",
                "",
                ":type ring: :py:class:`.QgsCurve`",
                ":param ring: The ring to be added",
                "",
                ":rtype: Qgis.GeometryOperationResult",
                ":return: OperationResult a result code: success or reason of failure",
                "",
            ],
        )

        # complex argument types
        lines = [
            "contains(self, element: Union[QDate, datetime.date]) -> bool",
            "Returns ``True`` if this range contains a specified ``element``.",
            "",
        ]

        AutoDocAdditions.process_docstring(
            app=None,
            what="method",
            name="qgis.core.QgsDateRange.contains",
            obj=dummy_method,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Returns ``True`` if this range contains a specified ``element``.",
                "",
                ":param element:",
                ":type element: Union[QDate, datetime.date]",
                "",
                ":rtype: bool",
            ],
        )

        # parenthesized tuple return type (issue #197)
        lines = [
            "transform(self, geometry: QgsGeometry, feedback: QgsFeedback = None) -> (QgsGeometry, bool)",
            "Transforms the specified input ``geometry``.",
            "",
            ":param geometry: Input geometry to transform",
            ":param feedback: optional feedback argument",
            "",
            ":return: - transformed geometry",
            "         - ok: ``True`` if geometry was successfully transformed",
            "",
        ]

        AutoDocAdditions.process_docstring(
            app=None,
            what="method",
            name="qgis.analysis.QgsGcpGeometryTransformer.transform",
            obj=dummy_method,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Transforms the specified input ``geometry``.",
                "",
                ":type geometry: :py:class:`.QgsGeometry`",
                ":param geometry: Input geometry to transform",
                ":type feedback: :py:class:`.QgsFeedback` = None",
                ":param feedback: optional feedback argument",
                "",
                ":rtype: (:py:class:`.QgsGeometry`, bool)",
                ":return: - transformed geometry",
                "         - ok: ``True`` if geometry was successfully transformed",
                "",
            ],
        )

    def test_process_docstring_for_classes(self):
        """
        Test logic for processing the docstrings for classes
        """

        class DummyClass:
            """
            xxx
            """

        lines = [
            "A geometry is the spatial representation of a feature.",
            "",
            ":py:class:`QgsGeometry` acts as a generic container for geometry",
            "objects. :py:class:`QgsGeometry` objects are implicitly shared, so",
            "making copies of geometries is inexpensive. The geometry container class",
            "can also be stored inside a QVariant object.",
            "",
            "The actual geometry representation is stored as a",
            ":py:class:`QgsAbstractGeometry` within the container, and can be",
            "accessed via the :py:func:`~get` method or set using the :py:func:`~set`",
            "method. This gives access to the underlying raw geometry primitive, such",
            "as the point, line, polygon, curve or other geometry subclasses.",
            "",
            ".. note::",
            "",
            "   :py:class:`QgsGeometry` objects are inherently Cartesian/planar geometries. They have no concept of geodesy, and none",
            "   of the methods or properties exposed from the :py:class:`QgsGeometry` API (or :py:class:`QgsAbstractGeometry` subclasses) utilize",
            "   geodesic calculations. Accordingly, properties like :py:func:`~length` and :py:func:`~area` or spatial operations like :py:func:`~buffer`",
            "   are always calculated using strictly Cartesian mathematics. In contrast, the :py:class:`QgsDistanceArea` class exposes",
            "   methods for working with geodesic calculations and spatial operations on geometries,",
            "   and should be used whenever calculations which account for the curvature of the Earth (or any other celestial body)",
            "   are required.",
            "",
            "QgsGeometry()",
            "",
            "QgsGeometry(QgsGeometry)",
            "Copy constructor will prompt a shallow copy of the geometry",
            "",
            "QgsGeometry(geom: QgsAbstractGeometry)",
            "Creates a geometry from an abstract geometry object. Ownership of geom",
            "is transferred.",
            "",
        ]

        AutoDocAdditions.process_docstring(
            app=None,
            what="class",
            name="qgis.core.QgsGeometry",
            obj=DummyClass,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                ".. py:method:: __init__()",
                "    :noindex:",
                "",
                "    ",
                ".. py:method:: __init__(QgsGeometry)",
                "    :noindex:",
                "",
                "    Copy constructor will prompt a shallow copy of the geometry",
                "    ",
                ".. py:method:: __init__(geom: QgsAbstractGeometry)",
                "    :noindex:",
                "",
                "    Creates a geometry from an abstract geometry object. Ownership of geom",
                "    is transferred.",
                "    ",
                "    :param geom:",
                "    :type geom: QgsAbstractGeometry",
            ],
        )

        # nested class
        lines = [
            "Contains additional contextual information about the context in which a",
            "callout is being rendered.",
            "",
            ".. versionadded:: 3.10",
            "",
        ]
        AutoDocAdditions.process_docstring(
            app=None,
            what="class",
            name="qgis.core.QgsCallout.QgsCalloutContext",
            obj=DummyClass,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Contains additional contextual information about the context in which a",
                "callout is being rendered.",
                "",
                ".. versionadded:: 3.10",
                "",
            ],
        )

    def test_process_docstring_for_signals(self):
        """
        Test logic for processing the docstrings for signals
        """

        class DummyClass:
            """
            xxx
            """

            fake_signal = ""

            __signal_arguments__ = {"autoRefreshIntervalChanged": ["interval: int"]}

        lines = [
            "Emitted when the auto refresh interval changes.",
            "",
            ".. seealso:: :py:func:`setAutoRefreshInterval`",
            "",
        ]

        AutoDocAdditions.PARENT_OBJ = DummyClass
        AutoDocAdditions.process_docstring(
            app=None,
            what="attribute",
            name="qgis.core.QgsMapLayer.autoRefreshIntervalChanged",
            obj=DummyClass.fake_signal,
            options={},
            lines=lines,
        )
        self.assertEqual(
            lines,
            [
                "Emitted when the auto refresh interval changes.",
                "",
                ".. seealso:: :py:func:`setAutoRefreshInterval`",
                "",
                ":param interval:",
                ":type interval: int",
            ],
        )
