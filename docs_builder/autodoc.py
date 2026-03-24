import enum
import pathlib
import re

import yaml
from docutils import nodes
from sphinx import addnodes
from sphinx.domains.python import PyAttribute, PyMethod
from sphinx.ext.autodoc import AttributeDocumenter, Documenter

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


old_documenter_get_doc = Documenter.get_doc
old_attribute_documenter_get_doc = AttributeDocumenter.get_doc
old_documenter_format_signature = Documenter.format_signature
old_py_method_get_signature_prefix = PyMethod.get_signature_prefix
old_py_attribute_get_signature_prefix = PyAttribute.get_signature_prefix


class AutoDocAdditions:

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
    def get_doc(self) -> list[list[str]] | None:
        """
        Attributes cannot have docstrings, so in QGIS we hack around this
        by storing them in a __attribute_docs__ dictionary in classes.

        This method is then monkey-patched into autodoc.Documenter
        to allow docstrings for attributes.
        """
        try:
            if self.object_name in self.parent.__attribute_docs__:
                docs = self.parent.__attribute_docs__[self.object_name]
                return [docs.split("\n")]
        except AttributeError:
            pass

        return old_documenter_get_doc(self)

    @staticmethod
    def attribute_get_doc(self):
        """
        This method is monkey-patched into autodoc.AttributeDocumenter as
        we need to make self.parent accessible to process_docstring -- this
        is a hacky approach to store it temporarily in a global. Sorry!
        """
        try:
            if self.object_name in self.parent.__attribute_docs__:
                AutoDocAdditions.PARENT_OBJ = self.parent
                docs = self.parent.__attribute_docs__[self.object_name]
                return [docs.split("\n")]
        except AttributeError:
            pass

        return old_attribute_documenter_get_doc(self)

    @staticmethod
    def format_signature(self, **kwargs) -> str:
        """
        Monkey patched into autodoc.Documenter for signature formatting,
        to retrieve signatures for signals, which are actually attributes
        and so don't have a real signature available!
        """
        try:
            if self.object_name in self.parent.__signal_arguments__:
                args = self.parent.__signal_arguments__[self.object_name]
                args = f'({", ".join(args)})'
                retann = None
                result = self.env.events.emit_firstresult(
                    "autodoc-process-signature",
                    self.objtype,
                    self.fullname,
                    self.object,
                    self.options,
                    args,
                    retann,
                )
                if result:
                    args, retann = result

                if args:
                    return args
                else:
                    return ""
        except AttributeError:
            pass

        return old_documenter_format_signature(self, **kwargs)

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


# monkey patch some Sphinx autodoc methods
# TODO -- is it possible to avoid this? Maybe a custom Documenter would help?
Documenter.format_signature = AutoDocAdditions.format_signature
Documenter.get_doc = AutoDocAdditions.get_doc
AttributeDocumenter.get_doc = AutoDocAdditions.attribute_get_doc
PyMethod.get_signature_prefix = AutoDocAdditions.method_get_signature_prefix
PyAttribute.get_signature_prefix = AutoDocAdditions.attribute_get_signature_prefix
