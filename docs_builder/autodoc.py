from __future__ import annotations

import enum
import pathlib
import re

import yaml
from docutils import nodes
from sphinx import addnodes
from sphinx.domains.python import PyAttribute, PyMethod

from .utils import Utils

try:
    from qgis._3d import *  # NOQA
    from qgis.analysis import *  # NOQA
    from qgis.core import *  # NOQA
    from qgis.gui import *  # NOQA
    from qgis.server import *  # NOQA
except ImportError:
    pass

with open(pathlib.Path(__file__).parent / ".." / "pyqgis_conf.yml") as f:
    cfg = yaml.safe_load(f)


old_py_method_get_signature_prefix = PyMethod.get_signature_prefix
old_py_attribute_get_signature_prefix = PyAttribute.get_signature_prefix

# Sphinx 9.x uses a new dynamic pipeline. Monkey-patch _get_docstring_lines
# to provide correct docstrings for pyqtSignal attributes, which would
# otherwise get the generic pyqtSignal docstring.
try:
    from sphinx.ext.autodoc._dynamic import _docstrings as _sphinx_docstrings

    _original_get_docstring_lines = _sphinx_docstrings._get_docstring_lines

    def _patched_get_docstring_lines(props, **kwargs):
        """Replace generic pyqtSignal docstrings with __attribute_docs__ content."""
        obj = props._obj
        if hasattr(obj, "__class__") and obj.__class__.__name__ == "pyqtSignal":
            parent = kwargs.get("parent")
            attr_name = props.name
            if parent and hasattr(parent, "__attribute_docs__"):
                if attr_name in parent.__attribute_docs__:
                    from sphinx.util.docstrings import prepare_docstring

                    docs = parent.__attribute_docs__[attr_name]
                    # Build a signature line so _extract_signatures_from_docstrings
                    # can extract it. Format: "attrName(arg1: type1, arg2: type2)"
                    sig_args = ""
                    if hasattr(parent, "__signal_arguments__"):
                        args_list = parent.__signal_arguments__.get(attr_name, [])
                        sig_args = ", ".join(args_list)
                    sig_line = f"{attr_name}({sig_args})"
                    full_doc = f"{sig_line}\n{docs}"
                    tab_width = kwargs.get("tab_width", 8)
                    return [prepare_docstring(full_doc, tab_width)]
        return _original_get_docstring_lines(props, **kwargs)

    _sphinx_docstrings._get_docstring_lines = _patched_get_docstring_lines

    # Also patch the reference in _loader.py which imported
    # _get_docstring_lines at module level
    from sphinx.ext.autodoc._dynamic import _loader as _sphinx_loader

    _sphinx_loader._get_docstring_lines = _patched_get_docstring_lines
except ImportError:
    # Sphinx < 9 — the dynamic pipeline doesn't exist
    pass


class AutoDocAdditions:

    @staticmethod
    def _get_parent_class(name: str):
        """
        Resolve the parent class from a fully qualified name like
        'qgis.core.QgsClass.attrName'. Wildcard imports put class names
        directly in globals, so look up the second-to-last part.
        """
        name_parts = name.split(".")
        if len(name_parts) >= 2:
            return globals().get(name_parts[-2])
        return None

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
        # autosummary may reference `__init__` on SIP-generated classes; the
        # imported obj is then `object.__init__`'s wrapper_descriptor whose
        # docstring is the generic "Initialize self." placeholder. There is
        # no signature to parse, so skip processing.
        if name.endswith(".__init__"):
            obj_doc = getattr(obj, "__doc__", "") or ""
            first_line = lines[0] if lines else obj_doc.split("\n", 1)[0]
            if first_line.startswith("Initialize self."):
                lines[:] = []
                return

        if what == "class":
            # SIP docstrings use the qualified class name minus the package,
            # e.g. "QgsGeometry" for qgis.core.QgsGeometry,
            #      "QgsFeatureRequest.OrderByClause" for qgis.core.QgsFeatureRequest.OrderByClause
            sip_class_name_escaped = re.escape(".".join(name.split(".")[2:]))
            is_nested = len(name.split(".")) > 3

            if not is_nested:
                # remove docstring part, we've already included it in the page header
                # only leave the __init__ methods
                init_idx = 0
                for init_idx, line in enumerate(lines):
                    if re.match(rf"^{sip_class_name_escaped}\(", line):
                        break
                lines[:] = lines[init_idx:]
            else:
                # For nested classes, check if constructors exist
                init_idx = None
                for idx, line in enumerate(lines):
                    if re.match(rf"^{sip_class_name_escaped}\(", line):
                        init_idx = idx
                        break

                if init_idx is None:
                    # No constructors found — keep docstring as-is with links
                    AutoDocAdditions.insert_links(lines)
                    return

                # Keep the class description, process constructors below
                description_part = lines[:init_idx]
                AutoDocAdditions.insert_links(description_part)
                lines[:] = lines[init_idx:]

            # loop through remaining lines, which are the constructors. Format
            # these up so they look like proper __init__ method documentation
            current_constructor = []
            current_constructor_args = []
            constructors = []
            for i, line in enumerate(lines):
                match = re.match(rf"^{sip_class_name_escaped}\((.*)\)", line)
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
                        re.sub(rf"^{sip_class_name_escaped}\(", ".. py:method:: __init__(", line)
                    )
                    # Only mark subsequent overloads as :noindex: so the first
                    # constructor remains cross-referenceable (e.g. by
                    # autoautosummary's `:init:` rubric).
                    if constructors:
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

            if is_nested:
                lines[:] = description_part
            else:
                lines[:] = []
            for constructor in constructors:
                lines.extend(constructor)
            return

        AutoDocAdditions.insert_links(lines)

        if what == "attribute":
            is_signal = hasattr(obj, "__class__") and obj.__class__.__name__ == "pyqtSignal"
            if is_signal:
                attr_name = name.split(".")[-1]
                parent_class = AutoDocAdditions._get_parent_class(name)

                # Replace generic pyqtSignal docstring with __attribute_docs__
                if parent_class and hasattr(parent_class, "__attribute_docs__"):
                    if attr_name in parent_class.__attribute_docs__:
                        docs = parent_class.__attribute_docs__[attr_name]
                        lines[:] = docs.split("\n")
                        AutoDocAdditions.insert_links(lines)

                # Inject signal argument types
                if parent_class and hasattr(parent_class, "__signal_arguments__"):
                    args = parent_class.__signal_arguments__.get(attr_name, [])
                    AutoDocAdditions.inject_args(args, lines)

        # add return type and param type
        elif what != "class" and not isinstance(obj, enum.EnumMeta) and obj.__doc__:
            # default to taking the signature from the lines we've already processed.
            # This is because we want the output processed earlier via the
            # OverloadedPythonMethodDocumenter class, so that we are only
            # looking at the docs relevant to the specific overload we are
            # currently processing
            signature = None
            parsed = None
            if lines:
                signature = lines[0]
            if signature:
                parsed = Utils.parse_signature(signature)
                if parsed[2] is not None:  # name component found
                    del lines[0]
                else:
                    parsed = None

            if parsed is None:
                signature = obj.__doc__.split("\n")[0]
                if signature == "":
                    return
                parsed = Utils.parse_signature(signature)
                if parsed[2] is None:
                    parsed = None

            if parsed is None:
                if name not in cfg["non-instantiable"]:
                    raise Warning(f"invalid signature for {name}: {signature}")

            else:
                _exmod, _path, _base, args, retann, _signal = parsed

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

    @staticmethod
    def process_signature(app, what, name, obj, options, signature, return_annotation):
        if what == "attribute":
            is_signal = hasattr(obj, "__class__") and obj.__class__.__name__ == "pyqtSignal"
            if is_signal:
                # In Sphinx 9.x, signature is None when the internal signatures
                # list is empty. Returning a value in that case would crash
                # Sphinx (IndexError on signatures[0]).
                if signature is None:
                    return None
                # Replace pyqtSignal's generic signature with
                # the correct signal arguments.
                attr_name = name.split(".")[-1]
                parent_class = AutoDocAdditions._get_parent_class(name)
                args_list = []
                if parent_class and hasattr(parent_class, "__signal_arguments__"):
                    args_list = parent_class.__signal_arguments__.get(attr_name, [])
                return f'({", ".join(args_list)})', None
        # we cannot render links in signature for the moment, so do nothing
        # https://github.com/sphinx-doc/sphinx/issues/1059
        return signature, return_annotation

    @staticmethod
    def skip_member(app, what, name, obj, skip, options):
        # skip monkey patched enums (base classes are different)
        if name == "staticMetaObject":
            return True
        if name == "baseClass":
            return True
        if hasattr(obj, "is_monkey_patched") and obj.is_monkey_patched:
            # print(f"skipping monkey patched enum {name}")
            return True
        return skip

    @staticmethod
    def process_bases(app, name, obj, option, bases: list) -> None:
        """Here we fine tune how the base class's classes are displayed."""
        for i, base in enumerate(bases):
            # replace 'sip.wrapper' base class with 'object'
            if base.__name__ == "wrapper":
                bases[i] = object

    @staticmethod
    def method_get_signature_prefix(self, sig: str):
        """
        Monkey patched into PyMethod.get_signature_prefix to tag
        abstract methods and virtual methods, using the
        __abstract_methods__ and __virtual_methods__ class members
        injected into the PyQGIS classes.

        Virtual methods are not supported natively by Sphinx,
        and abstract methods from sip bindings are not detected by Sphinx.
        """
        prefix = old_py_method_get_signature_prefix(self, sig)

        # find actual class and name for the method
        assert len(self.arguments) == 1
        name_parts = self.arguments[0].split("(")[0]
        obj_class, method_name = Utils.get_class_from_fully_qualified_attribute_name(
            name_parts, globals()
        )

        if obj_class:
            # check if method is present in the __abstract_methods__,
            # __virtual_methods__ or __overridden_methods__ class
            # members, and if so, add appropriate prefix tags
            if (
                hasattr(obj_class, method_name)
                and hasattr(obj_class, "__abstract_methods__")
                and method_name in obj_class.__abstract_methods__
            ):
                prefix.append(nodes.Text("abstract"))
                prefix.append(addnodes.desc_sig_space())
            elif hasattr(obj_class, method_name) and (
                (
                    hasattr(obj_class, "__virtual_methods__")
                    and method_name in obj_class.__virtual_methods__
                )
                or (
                    hasattr(obj_class, "__overridden_methods__")
                    and method_name in obj_class.__overridden_methods__
                )
            ):
                prefix.append(nodes.Text("virtual"))
                prefix.append(addnodes.desc_sig_space())

        return prefix

    @staticmethod
    def attribute_get_signature_prefix(self, sig: str):
        """
        Monkey patched into PyAttribute.get_signature_prefix to tag
        signals, which are not supported natively by Sphinx.
        """
        prefix = old_py_attribute_get_signature_prefix(self, sig)

        # find actual class and name for the attribute
        assert len(self.arguments) == 1
        name_parts = self.arguments[0].split("(")[0]
        obj_class, method_name = Utils.get_class_from_fully_qualified_attribute_name(
            name_parts, globals()
        )

        if obj_class:
            # does this attribute look like a signal?
            if (
                hasattr(obj_class, method_name)
                and getattr(obj_class, method_name).__class__.__name__ == "pyqtSignal"
            ):
                prefix.append(nodes.Text("signal"))
                prefix.append(addnodes.desc_sig_space())

        return prefix


# Monkey-patch Python domain classes to add abstract/virtual/signal prefixes.
# These domain classes (PyMethod, PyAttribute) are unchanged in Sphinx 9.x.
PyMethod.get_signature_prefix = AutoDocAdditions.method_get_signature_prefix
PyAttribute.get_signature_prefix = AutoDocAdditions.attribute_get_signature_prefix
