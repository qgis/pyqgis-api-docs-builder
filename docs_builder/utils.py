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
    def parse_signature(
        signature: str,
    ) -> tuple[str | None, str | None, str | None, str | None, str | None, bool]:
        """
        Parses a SIP-generated method signature string into its components,
        correctly handling nested parentheses in arguments and return types.

        Returns a tuple of (explicit_module, path, name, args, return_annotation, is_signal).
        Returns None for any component that is not present.

        Uses bracket-depth tracking instead of regex so that parenthesized
        return types like ``-> (QgsGeometry, bool)`` are not swallowed
        into the argument list.
        """
        s = signature.strip()
        if not s:
            return None, None, None, None, None, False

        # Find the opening '(' for arguments
        paren_pos = s.find("(")
        if paren_pos < 0:
            return None, None, None, None, None, False

        leading = s[:paren_pos].strip()
        if not leading:
            return None, None, None, None, None, False

        # Split leading into explicit_module, path, name
        explicit_module = None
        if "::" in leading:
            explicit_module, leading = leading.split("::", 1)

        parts = leading.rsplit(".", 1)
        if len(parts) == 2:
            path = parts[0] + "."
            name = parts[1]
        else:
            path = None
            name = parts[0]

        if not name or not name.replace("_", "").isalnum():
            return None, None, None, None, None, False

        # Walk character by character from the opening '(' to find the
        # matching ')' respecting nested brackets
        depth = 0
        args_end = None
        for i in range(paren_pos, len(s)):
            ch = s[i]
            if ch in ("(", "["):
                depth += 1
            elif ch in (")", "]"):
                depth -= 1
                if depth == 0:
                    args_end = i
                    break

        if args_end is None:
            return None, None, None, None, None, False

        args = s[paren_pos + 1 : args_end]

        remainder = s[args_end + 1 :].strip()

        # Extract return annotation
        return_annotation = None
        if remainder.startswith("->"):
            remainder = remainder[2:].strip()
            # Check for [signal] suffix
            if remainder.endswith("[signal]"):
                return_annotation = remainder[: -len("[signal]")].strip()
                return explicit_module, path, name, args, return_annotation, True
            else:
                return_annotation = remainder if remainder else None
                return explicit_module, path, name, args, return_annotation, False

        # Check for [signal] without return annotation
        is_signal = False
        if remainder.strip() == "[signal]":
            is_signal = True

        return explicit_module, path, name, args, return_annotation, is_signal

    @staticmethod
    def get_class_from_fully_qualified_attribute_name(
        name: str, module_globals: dict[str, Any]
    ) -> tuple[type | None, str]:
        """
        Given the fully-qualified name of an attribute, returns the fully-qualified
        name of the class that the object belongs to and the attribute name
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
                return _class, ".".join(name_parts[len(try_class_name_parts) - 1 :])

        return None, ""
