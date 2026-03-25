"""
Test autodoc additions
"""

import unittest

from docs_builder.autodoc import AutoDocAdditions


def _inject_class(cls):
    """
    Register a class in the autodoc module's globals, mimicking what
    ``from qgis.core import *`` does in production. Returns a cleanup
    function to be called afterwards.
    """
    import docs_builder.autodoc as autodoc_mod

    autodoc_mod.__dict__[cls.__name__] = cls
    return lambda: autodoc_mod.__dict__.pop(cls.__name__, None)


class TestProcessDocstringMethods(unittest.TestCase):
    """Tests for process_docstring on methods (link insertion, param/rtype injection)"""

    def _process_method(self, name, lines):
        def dummy():
            """addFeature(self) -> bool"""

        AutoDocAdditions.process_docstring(
            app=None, what="method", name=name, obj=dummy, options={}, lines=lines
        )

    def test_class_links_inserted(self):
        lines = [
            "addFeature(self) -> bool",
            "Adds a single ``feature`` to the sink.",
            "",
            ".. seealso:: QgsVectorLayer for another class",
            "",
        ]
        self._process_method("qgis.core.QgsFeatureSink.addFeature", lines)
        self.assertIn(".. seealso:: :py:class:`.QgsVectorLayer` for another class", lines)

    def test_links_not_inserted_in_code_blocks(self):
        lines = [
            "addFeature(self) -> bool",
            "Example:",
            "",
            ".. code-block:",
            "",
            "  class MyClass(QgsMapLayer):",
            "    pass",
            "",
            "",
        ]
        self._process_method("qgis.core.QgsFeatureSink.addFeature", lines)
        # Inside code block, class names should not be linked
        self.assertIn("  class MyClass(QgsMapLayer):", lines)

    def test_overloaded_signature_parsed(self):
        lines = [
            "addRing(self, ring: Iterable[QgsPointXY]) -> Qgis.GeometryOperationResult",
            "Adds a new ring to this geometry.",
            "",
            ":param ring: The ring to be added",
            "",
            ":return: result code",
            "",
        ]
        self._process_method("qgis.core.QgsGeometry.addRing", lines)
        self.assertIn(":type ring: Iterable[QgsPointXY]", lines)
        self.assertIn(":rtype: Qgis.GeometryOperationResult", lines)
        # Signature line should have been consumed
        self.assertNotIn(
            "addRing(self, ring: Iterable[QgsPointXY]) -> Qgis.GeometryOperationResult",
            lines,
        )

    def test_qgis_class_type_linked(self):
        lines = [
            "addRing(self, ring: QgsCurve) -> Qgis.GeometryOperationResult",
            "Adds a new ring.",
            "",
            ":param ring: The ring to be added",
            "",
        ]
        self._process_method("qgis.core.QgsGeometry.addRing", lines)
        self.assertIn(":type ring: :py:class:`.QgsCurve`", lines)

    def test_complex_union_argument(self):
        lines = [
            "contains(self, element: Union[QDate, datetime.date]) -> bool",
            "Returns ``True`` if this range contains a specified ``element``.",
            "",
        ]
        self._process_method("qgis.core.QgsDateRange.contains", lines)
        self.assertIn(":type element: Union[QDate, datetime.date]", lines)
        self.assertIn(":rtype: bool", lines)

    def test_parenthesized_tuple_return_type(self):
        """Regression test for issue #197 — tuple return types like -> (QgsGeometry, bool)"""
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
        self._process_method("qgis.analysis.QgsGcpGeometryTransformer.transform", lines)
        self.assertIn(":rtype: (:py:class:`.QgsGeometry`, bool)", lines)
        self.assertIn(":type geometry: :py:class:`.QgsGeometry`", lines)


class TestProcessDocstringClasses(unittest.TestCase):
    """Tests for process_docstring on classes (constructor formatting)"""

    def test_constructors_formatted(self):
        class DummyClass:
            """xxx"""

        lines = [
            "A geometry is the spatial representation of a feature.",
            "",
            "QgsGeometry()",
            "",
            "QgsGeometry(QgsGeometry)",
            "Copy constructor",
            "",
            "QgsGeometry(geom: QgsAbstractGeometry)",
            "Creates a geometry from an abstract geometry object.",
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
        self.assertIn(".. py:method:: __init__()", lines)
        self.assertIn(".. py:method:: __init__(QgsGeometry)", lines)
        self.assertIn(".. py:method:: __init__(geom: QgsAbstractGeometry)", lines)
        self.assertIn("    :type geom: QgsAbstractGeometry", lines)
        # Original class description should be removed
        self.assertNotIn("A geometry is the spatial representation of a feature.", lines)

    def test_nested_class_preserved(self):
        class DummyClass:
            """xxx"""

        lines = [
            "Contains additional contextual information.",
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
        # Nested classes should keep their docstring intact
        self.assertIn("Contains additional contextual information.", lines)

    def test_nested_class_with_constructors(self):
        """Nested classes with constructors should format them as __init__ methods."""

        class DummyClass:
            """xxx"""

        lines = [
            "The OrderByClause class represents an order by clause.",
            "",
            "QgsFeatureRequest.OrderByClause(expression: Optional[str], ascending: bool = True)",
            "Creates a new OrderByClause",
            "",
            ":param expression: The expression to use for ordering",
            ":param ascending: If the order should be ascending",
            "",
            "QgsFeatureRequest.OrderByClause(expression: QgsExpression, ascending: bool, nullsfirst: bool)",
            "Creates a new OrderByClause with nulls ordering",
            "",
            ":param expression: The expression to use for ordering",
            ":param ascending: If the order should be ascending",
            ":param nullsfirst: If True, NULLS are at the beginning",
            "",
            "QgsFeatureRequest.OrderByClause(a0: QgsFeatureRequest.OrderByClause)",
            "",
        ]
        AutoDocAdditions.process_docstring(
            app=None,
            what="class",
            name="qgis.core.QgsFeatureRequest.OrderByClause",
            obj=DummyClass,
            options={},
            lines=lines,
        )
        # Description should be preserved for nested classes
        self.assertIn("The OrderByClause class represents an order by clause.", lines)
        # Constructors should be formatted as __init__
        self.assertIn(
            ".. py:method:: __init__(expression: Optional[str], ascending: bool = True)",
            lines,
        )
        self.assertIn(
            ".. py:method:: __init__(expression: QgsExpression, ascending: bool, nullsfirst: bool)",
            lines,
        )
        self.assertIn(".. py:method:: __init__(a0: QgsFeatureRequest.OrderByClause)", lines)
        # Type annotations should be injected
        self.assertIn("    :type expression: Optional[str]", lines)
        # The raw SIP signature lines should be gone
        self.assertNotIn(
            "QgsFeatureRequest.OrderByClause(expression: Optional[str], ascending: bool = True)",
            lines,
        )


class TestProcessDocstringSignals(unittest.TestCase):
    """Tests for process_docstring on signals (attribute docs, argument injection)"""

    def test_signal_args_injected(self):
        class pyqtSignal:
            """Generic pyqtSignal docstring"""

        class DummyClass:
            autoRefreshIntervalChanged = pyqtSignal()
            __attribute_docs__ = {
                "autoRefreshIntervalChanged": "Emitted when the auto refresh interval changes."
            }
            __signal_arguments__ = {"autoRefreshIntervalChanged": ["interval: int"]}

        cleanup = _inject_class(DummyClass)
        try:
            lines = ["Emitted when the auto refresh interval changes."]
            AutoDocAdditions.process_docstring(
                app=None,
                what="attribute",
                name="qgis.core.DummyClass.autoRefreshIntervalChanged",
                obj=DummyClass.autoRefreshIntervalChanged,
                options={},
                lines=lines,
            )
            self.assertIn(":param interval:", lines)
            self.assertIn(":type interval: int", lines)
        finally:
            cleanup()

    def test_generic_pyqtsignal_docstring_replaced(self):
        """Sphinx 9.x sends generic pyqtSignal docstring — should be replaced."""

        class pyqtSignal:
            """Generic pyqtSignal docstring"""

        class DummySignalClass:
            mySignal = pyqtSignal()
            __attribute_docs__ = {
                "mySignal": ("Emitted when something changes.\n" "\n" ".. versionadded:: 3.26\n")
            }
            __signal_arguments__ = {"mySignal": []}

        cleanup = _inject_class(DummySignalClass)
        try:
            lines = [
                "pyqtSignal(*types, name: str = ..., revision: int = ..., arguments: Sequence = ...) -> PYQT_SIGNAL",
                "",
                "types is normally a sequence of individual types.",
                "",
            ]
            AutoDocAdditions.process_docstring(
                app=None,
                what="attribute",
                name="qgis.core.DummySignalClass.mySignal",
                obj=DummySignalClass.mySignal,
                options={},
                lines=lines,
            )
            self.assertIn("Emitted when something changes.", lines)
            self.assertIn(".. versionadded:: 3.26", lines)
            # Generic docstring should be gone
            self.assertNotIn("types is normally a sequence of individual types.", lines)
        finally:
            cleanup()


class TestProcessSignature(unittest.TestCase):
    """Tests for process_signature (signal signature replacement)"""

    def test_signal_no_args(self):
        class pyqtSignal:
            """Generic pyqtSignal docstring"""

        class DummyClass:
            noArgsSignal = pyqtSignal()
            __signal_arguments__ = {"noArgsSignal": []}

        cleanup = _inject_class(DummyClass)
        try:
            result = AutoDocAdditions.process_signature(
                app=None,
                what="attribute",
                name="qgis.core.DummyClass.noArgsSignal",
                obj=DummyClass.noArgsSignal,
                options={},
                signature="(*types, name: str = ...)",
                return_annotation="PYQT_SIGNAL",
            )
            self.assertEqual(result, ("()", None))
        finally:
            cleanup()

    def test_signal_with_args(self):
        class pyqtSignal:
            """Generic pyqtSignal docstring"""

        class DummyClass:
            oneArgSignal = pyqtSignal()
            __signal_arguments__ = {"oneArgSignal": ["value: int"]}

        cleanup = _inject_class(DummyClass)
        try:
            result = AutoDocAdditions.process_signature(
                app=None,
                what="attribute",
                name="qgis.core.DummyClass.oneArgSignal",
                obj=DummyClass.oneArgSignal,
                options={},
                signature="(*types, name: str = ...)",
                return_annotation="PYQT_SIGNAL",
            )
            self.assertEqual(result, ("(value: int)", None))
        finally:
            cleanup()

    def test_signal_signature_none_returns_none(self):
        """In Sphinx 9.x, signature=None when internal signatures list is empty."""

        class pyqtSignal:
            """Generic pyqtSignal docstring"""

        class DummyClass:
            sig = pyqtSignal()
            __signal_arguments__ = {"sig": []}

        cleanup = _inject_class(DummyClass)
        try:
            result = AutoDocAdditions.process_signature(
                app=None,
                what="attribute",
                name="qgis.core.DummyClass.sig",
                obj=DummyClass.sig,
                options={},
                signature=None,
                return_annotation=None,
            )
            self.assertIsNone(result)
        finally:
            cleanup()

    def test_method_signature_passthrough(self):
        result = AutoDocAdditions.process_signature(
            app=None,
            what="method",
            name="qgis.core.SomeClass.method",
            obj=lambda: None,
            options={},
            signature="(self, arg: str)",
            return_annotation="bool",
        )
        self.assertEqual(result, ("(self, arg: str)", "bool"))


if __name__ == "__main__":
    unittest.main()
