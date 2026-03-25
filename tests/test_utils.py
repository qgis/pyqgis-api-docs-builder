"""
Test utilities
"""

import unittest

from docs_builder.utils import Utils


class TestClass:
    attribute = "test"

    class NestedClass:
        nested_attribute = "nested"

    def test_method(self):
        pass


class OuterModule:
    class InnerClass:
        inner_attribute = "inner"


class ComplexHierarchy:
    class Level1:
        class Level2:
            class Level3:
                deep_attribute = "deep"


class TestUtils(unittest.TestCase):
    """
    Test Utils class
    """

    def test_split_to_tokens(self):
        # Simple comma-separated string without brackets
        self.assertEqual(Utils.split_to_tokens("a, b, c"), ["a", "b", "c"])

        self.assertEqual(
            Utils.split_to_tokens("self, element: Union[QDate, datetime.date]"),
            ["self", "element: Union[QDate, datetime.date]"],
        )

        # Nested brackets
        self.assertEqual(Utils.split_to_tokens("a, b[c, d[e, f]], g"), ["a", "b[c, d[e, f]]", "g"])

        # Mixed nested brackets
        self.assertEqual(Utils.split_to_tokens("a, b[c, d(e, f)], g"), ["a", "b[c, d(e, f)]", "g"])

        # Empty string
        self.assertEqual(Utils.split_to_tokens(""), [])

        # No commas
        self.assertEqual(Utils.split_to_tokens("abcdef"), ["abcdef"])

        # Starting with comma
        self.assertEqual(Utils.split_to_tokens(", a, b"), ["", "a", "b"])

        # Ending with comma
        self.assertEqual(Utils.split_to_tokens("a, b, "), ["a", "b"])

        # Multiple types of brackets
        self.assertEqual(
            Utils.split_to_tokens("a, func(x, y), c[d, e]"), ["a", "func(x, y)", "c[d, e]"]
        )

        # Unbalanced brackets
        self.assertEqual(Utils.split_to_tokens("a, b[c, d"), ["a", "b[c, d"])

        # Whitespace handling
        self.assertEqual(Utils.split_to_tokens("  a  ,  b[c, d]  ,  e  "), ["a", "b[c, d]", "e"])

    def test_get_class_from_fully_qualified_attribute_name(self):
        """
        Test Utils.get_class_from_fully_qualified_attribute_name
        """

        # Basic attribute lookup
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "TestClass.attribute", globals()
        )
        self.assertEqual(result, (TestClass, "attribute"))

        # Nested class attribute
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "TestClass.NestedClass.nested_attribute", globals()
        )
        self.assertEqual(result, (TestClass.NestedClass, "nested_attribute"))

        # Double nested class
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "OuterModule.InnerClass.inner_attribute", globals()
        )
        self.assertEqual(result, (OuterModule.InnerClass, "inner_attribute"))

        # Nonexistent attribute
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "NonexistentClass.attribute", globals()
        )
        self.assertEqual(result, (None, ""))

        # Nonexistent nested attribute
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "TestClass.NonexistentNestedClass.attribute", globals()
        )
        self.assertEqual(result, (TestClass, "NonexistentNestedClass.attribute"))

        # Single name no dots
        result = Utils.get_class_from_fully_qualified_attribute_name("SingleName", globals())
        self.assertEqual(result, (None, ""))

        # Empty string
        result = Utils.get_class_from_fully_qualified_attribute_name("", globals())
        self.assertEqual(result, (None, ""))

        # With method name instead of attribute
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "TestClass.test_method", globals()
        )
        self.assertEqual(result, (TestClass, "test_method"))

        # With complicated hierarchy
        result = Utils.get_class_from_fully_qualified_attribute_name(
            "ComplexHierarchy.Level1.Level2.Level3.deep_attribute", globals()
        )
        self.assertEqual(result, (ComplexHierarchy.Level1.Level2.Level3, "deep_attribute"))

    def test_parse_signature(self):
        """
        Test Utils.parse_signature
        """
        # Simple method with return type
        self.assertEqual(
            Utils.parse_signature("method(self, arg: str) -> bool"),
            (None, None, "method", "self, arg: str", "bool", False),
        )

        # Parenthesized tuple return type (issue #197)
        self.assertEqual(
            Utils.parse_signature(
                "transform(self, geometry: QgsGeometry, feedback: QgsFeedback = None) -> (QgsGeometry, bool)"
            ),
            (
                None,
                None,
                "transform",
                "self, geometry: QgsGeometry, feedback: QgsFeedback = None",
                "(QgsGeometry, bool)",
                False,
            ),
        )

        # Tuple[] return type
        self.assertEqual(
            Utils.parse_signature("loadNamedStyle(self, uri: Optional[str]) -> Tuple[str, bool]"),
            (None, None, "loadNamedStyle", "self, uri: Optional[str]", "Tuple[str, bool]", False),
        )

        # Complex args with nested parens in default values
        self.assertEqual(
            Utils.parse_signature(
                "getFeatures(self, request: QgsFeatureRequest = QgsFeatureRequest()) -> QgsFeatureIterator"
            ),
            (
                None,
                None,
                "getFeatures",
                "self, request: QgsFeatureRequest = QgsFeatureRequest()",
                "QgsFeatureIterator",
                False,
            ),
        )

        # No return type
        self.assertEqual(
            Utils.parse_signature(
                "setGcpTransformer(self, transformer: QgsGcpTransformerInterface)"
            ),
            (
                None,
                None,
                "setGcpTransformer",
                "self, transformer: QgsGcpTransformerInterface",
                None,
                False,
            ),
        )

        # Signal
        self.assertEqual(
            Utils.parse_signature("mySignal(self, arg: str) -> None [signal]"),
            (None, None, "mySignal", "self, arg: str", "None", True),
        )

        # Module-qualified name
        self.assertEqual(
            Utils.parse_signature("qgis.core.QgsProject.instance() -> QgsProject"),
            (None, "qgis.core.QgsProject.", "instance", "", "QgsProject", False),
        )

        # No arguments, no return type
        self.assertEqual(
            Utils.parse_signature("instance()"),
            (None, None, "instance", "", None, False),
        )

        # Empty string
        self.assertEqual(
            Utils.parse_signature(""),
            (None, None, None, None, None, False),
        )

        # No parentheses — not a valid signature
        self.assertEqual(
            Utils.parse_signature("just_a_name"),
            (None, None, None, None, None, False),
        )

        # Explicit module prefix
        self.assertEqual(
            Utils.parse_signature("qgis.core::QgsProject.instance() -> QgsProject"),
            ("qgis.core", "QgsProject.", "instance", "", "QgsProject", False),
        )


if __name__ == "__main__":
    unittest.main()
