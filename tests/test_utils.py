"""
Test utilities
"""

import unittest

from docs_builder.utils import Utils


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


if __name__ == "__main__":
    unittest.main()
