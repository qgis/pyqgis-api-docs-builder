"""
Contains utility functions for documentation logic
"""

from typing import Any


class Utils:
    """
    Contains utility functions for documentation logic
    """

    @staticmethod
    def split_to_tokens(string: str, separator: str = ",") -> list[str]:
        """
        Splits a string to a list of tokens, correctly handling
        separators which should be ignored as they are inside
        pairs of matching [] or () brackets
        """
        tokens = []
        current_token = ""
        depth = 0

        for char in string:
            if char == separator and depth == 0:
                tokens.append(current_token.strip())
                current_token = ""
            else:
                current_token += char
                if char in ("[", "("):
                    depth += 1
                elif char in ("]", ")"):
                    depth -= 1

        if current_token.strip():
            tokens.append(current_token.strip())

        return tokens

    @staticmethod
    def get_class_from_fully_qualified_attribute_name(
        name: str, module_globals: dict[str, Any]
    ) -> type | None:
        """
        Given the fully-qualified name of an attribute, returns the fully-qualified
        name of the class that the object belongs to.
        """
        name_parts = name.split(".")
        _class = None
        if len(name_parts) > 1:
            try_class_name_parts = name_parts[:]
            while try_class_name_parts:
                try:
                    _class = module_globals[".".join(try_class_name_parts)]
                    break
                except KeyError:
                    try_class_name_parts = try_class_name_parts[:-1]

            if _class is not None:
                while len(try_class_name_parts) < len(name_parts):
                    try_class_name_parts.append(name_parts[len(try_class_name_parts)])
                    if hasattr(_class, try_class_name_parts[-1]) and isinstance(
                        getattr(_class, try_class_name_parts[-1]), type
                    ):
                        _class = getattr(_class, try_class_name_parts[-1])
                    else:
                        break
                return _class

        return None
