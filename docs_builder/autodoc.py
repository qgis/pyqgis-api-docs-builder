import enum
import pathlib
import re

import yaml

from .utils import Utils

with open(pathlib.Path(__file__).parent / ".." / "pyqgis_conf.yml") as f:
    cfg = yaml.safe_load(f)


class AutoDocAdditions:
    # https://github.com/sphinx-doc/sphinx/blob/685e3fdb49c42b464e09ec955e1033e2a8729fff/sphinx/ext/autodoc/__init__.py#L51
    # adapted to handle signals

    # https://regex101.com/r/lSB3rK/2/
    py_ext_sig_re = re.compile(
        r"""^ ([\w.]+::)?            # explicit module name
              ([\w.]+\.)?            # module and/or class name(s)
              (\w+)  \s*             # thing name
              (?: \((.*)\)          # optional: arguments
              (?:\s* -> \s* ([\w.]+(?:\[.*?])?))?   # return annotation
              (?:\s* \[(signal)])?    # is signal
              )? $                   # and nothing more
              """,
        re.VERBOSE,
    )

    # hack
    PARENT_OBJ = None

    @staticmethod
    def create_links(doc: str) -> str:
        # fix inheritance
        doc = re.sub(r"qgis\._(core|gui|analysis|processing)\.", r"", doc)
        # class
        doc = re.sub(r"\b(Qgi?s[A-Z]\w+)([, )]|\. )", r":py:class:`.\1`\2", doc)
        return doc

    @staticmethod
    def insert_links(lines: list[str]):
        """
        Inserts link tags into a block of docstring lines
        """
        in_code_block = False
        for i in range(len(lines)):
            # fix seealso
            # lines[i] = re.sub(r':py: func:`(\w+\(\))`', r':func:`.{}.\1()'.format(what), lines[i])
            if lines[i].startswith(".. code-block"):
                in_code_block = True
            elif not lines[i] and i < len(lines) - 1 and not lines[i + 1]:
                in_code_block = False

            if not in_code_block:
                lines[i] = AutoDocAdditions.create_links(lines[i])

    @staticmethod
    def inject_args(args: list[str], lines: list[str], indent: int = 0):
        """
        Injects :param and param :type lines into a docstring, for the
        arguments specified in args
        """
        for arg in args:
            try:
                arg_name, hint = arg.split(": ")
            except ValueError:
                continue
            search_for = f":param {arg_name}:"
            insert_index = None

            for i, line in enumerate(lines):
                if line.strip().startswith(search_for):
                    insert_index = i
                    break

            if insert_index is None:
                lines.append((" " * indent) + search_for)
                insert_index = len(lines)

            if insert_index is not None:
                lines.insert(
                    insert_index,
                    f"{' ' * indent}:type {arg_name}: {AutoDocAdditions.create_links(hint)}",
                )

    @staticmethod
    def process_docstring(app, what, name, obj, options, lines):
        if what == "class":
            # hacky approach to detect nested classes, eg QgsCallout.QgsCalloutContext
            is_nested = len(name.split(".")) > 3
            if not is_nested:
                # remove docstring part, we've already included it in the page header
                # only leave the __init__ methods
                init_idx = 0
                class_name = name.split(".")[-1]
                for init_idx, line in enumerate(lines):
                    if re.match(rf"^{class_name}\(", line):
                        break

                lines[:] = lines[init_idx:]
                # loop through remaining lines, which are the constructors. Format
                # these up so they look like proper __init__ method documentation
                current_constructor = []
                current_constructor_args = []
                constructors = []
                for i, line in enumerate(lines):
                    match = re.match(rf"^{class_name}\((.*)\)", line)
                    if match:
                        if current_constructor:
                            if current_constructor_args:
                                AutoDocAdditions.inject_args(
                                    current_constructor_args, current_constructor, indent=4
                                )
                            constructors.append(current_constructor)
                            current_constructor = []
                        current_constructor_args = Utils.split_to_tokens(match.group(1))
                        current_constructor.append(
                            re.sub(rf"\b{class_name}\(", ".. py:method:: __init__(", line)
                        )
                        current_constructor.append("    :noindex:")
                        current_constructor.append("")
                    else:
                        current_constructor.append("    " + line)
                if current_constructor:
                    if current_constructor_args:
                        AutoDocAdditions.inject_args(
                            current_constructor_args, current_constructor, indent=4
                        )
                    constructors.append(current_constructor)

                lines[:] = []
                for constructor in constructors:
                    lines.extend(constructor)
                return

        AutoDocAdditions.insert_links(lines)

        if what == "attribute":
            try:
                args = AutoDocAdditions.PARENT_OBJ.__signal_arguments__.get(
                    name.split(".")[-1], []
                )
                AutoDocAdditions.inject_args(args, lines)
            except AttributeError:
                pass

        # add return type and param type
        elif what != "class" and not isinstance(obj, enum.EnumMeta) and obj.__doc__:
            # default to taking the signature from the lines we've already processed.
            # This is because we want the output processed earlier via the
            # OverloadedPythonMethodDocumenter class, so that we are only
            # looking at the docs relevant to the specific overload we are
            # currently processing
            signature = None
            match = None
            if lines:
                signature = lines[0]
            if signature:
                match = AutoDocAdditions.py_ext_sig_re.match(signature)
                if match:
                    del lines[0]

            if match is None:
                signature = obj.__doc__.split("\n")[0]
                if signature == "":
                    return
                match = AutoDocAdditions.py_ext_sig_re.match(signature)

            if match is None:
                if name not in cfg["non-instantiable"]:
                    raise Warning(f"invalid signature for {name}: {signature}")

            else:
                exmod, path, base, args, retann, signal = match.groups()

                if args:
                    args = Utils.split_to_tokens(args)
                    AutoDocAdditions.inject_args(args, lines)

                if retann:
                    insert_index = len(lines)
                    for i, line in enumerate(lines):
                        if line.startswith(":rtype:"):
                            insert_index = None
                            break
                        elif line.startswith(":return:") or line.startswith(":returns:"):
                            insert_index = i

                    if insert_index is not None:
                        if insert_index == len(lines):
                            # Ensure that :rtype: doesn't get joined with a paragraph of text, which
                            # prevents it being interpreted.
                            lines.append("")
                            insert_index += 1

                        lines.insert(
                            insert_index, f":rtype: {AutoDocAdditions.create_links(retann)}"
                        )
