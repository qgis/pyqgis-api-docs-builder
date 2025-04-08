"""
Contains utility functions for documentation logic
"""


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
