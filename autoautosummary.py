# creates methods summary
# see https://stackoverflow.com/questions/20569011/python-sphinx-autosummary-automated-listing-of-member-functions
# added toctree and nosignatures in options

import re
from enum import Enum
from typing import Any

from docutils import nodes
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser, directives
from docutils.utils import new_document
from qgis.PyQt.QtCore import pyqtSignal as _pyqtSignal
from sphinx.ext import autosummary

# Sphinx 9.x made get_documenter private and changed its signature
from sphinx.ext.autosummary import Autosummary, ImportExceptionGroup
from sphinx.ext.autosummary import _get_documenter as _sphinx_get_documenter
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.inspect import isstaticmethod, safe_getattr


def _get_documenter_type(app, obj, parent):
    result = _sphinx_get_documenter(obj, parent)
    # Sphinx 9.x returns a string directly
    if isinstance(result, str):
        return result
    return result.objtype


# from sphinx.directives import directive
logger = logging.getLogger(__name__)


old_extract_summary = autosummary.extract_summary


def new_extract_summary(doc: list[str], document: Any) -> str:
    res = old_extract_summary(doc, document)
    # we only want to remove the surrounding ` from argument names here.
    # So we don't want to match:
    # - literals, e.g. None, True, False
    # - :py: directives (e.g. links to other classes)
    res = re.sub(r"(?<!:)`((?!None|True|False)[a-zA-Z0-9_]+)`", r"\1", res)
    return res


autosummary.extract_summary = new_extract_summary


class AutoAutoSummary(Autosummary):
    """
    Create a summary for methods, attributes, signals, virtual and abstract methods (autosummary).

    If the summary contains elements, a title (Methods, Attributes or Signals)
    is automatically added before (using the rubric directive).

    see https://stackoverflow.com/questions/20569011/python-sphinx-autosummary-automated-listing-of-member-functions
    """

    option_spec = {
        "methods": directives.unchanged,
        "static_methods": directives.unchanged,
        "signals": directives.unchanged,
        "virtual_methods": directives.unchanged,
        "abstract_methods": directives.unchanged,
        "classes": directives.unchanged,
        "enums": directives.unchanged,
        "attributes": directives.unchanged,
        "nosignatures": directives.unchanged,
        "toctree": directives.unchanged,
        "exclude-members": directives.unchanged,
    }

    required_arguments = 1

    @staticmethod
    def skip_member(doc, obj: Any, name: str, options, objtype: str) -> bool:
        # print(name, name in options.get('exclude-members', '').split(','))
        try:
            if name in options.get("exclude-members", "").split(","):
                return True
            return doc.settings.env.app.emit_firstresult(
                "autodoc-skip-member", objtype, name, obj, False, {}
            )
        except Exception as exc:
            logger.warning(
                __(
                    "autosummary: failed to determine %r to be documented."
                    "the following exception was raised:\n%s"
                ),
                name,
                exc,
                type="autosummary",
            )
            return False

    @staticmethod
    def get_members(
        doc,
        obj,
        typ,
        options,
        include_public: list | None = None,
        signal=False,
        enum=False,
        static=False,
        virtual=False,
        abstract=False,
    ):
        try:
            if not include_public:
                include_public = []
            items = []

            for name in dir(obj):
                if name not in obj.__dict__.keys():
                    continue
                try:
                    chobj = safe_getattr(obj, name)

                    abstract_methods = (
                        obj.__abstract_methods__ if hasattr(obj, "__abstract_methods__") else set()
                    )
                    virtual_methods = (
                        obj.__virtual_methods__ if hasattr(obj, "__virtual_methods__") else set()
                    )
                    overridden_methods = (
                        obj.__overridden_methods__
                        if hasattr(obj, "__overridden_methods__")
                        else set()
                    )

                    objtype = _get_documenter_type(doc.settings.env.app, chobj, obj)
                    if objtype == typ:
                        skipped = AutoAutoSummary.skip_member(doc, chobj, name, options, objtype)
                        if skipped is True:
                            continue
                        if typ == "method":
                            method_is_static = isstaticmethod(chobj, obj, name)
                            if method_is_static != static:
                                continue
                            method_is_abstract = name in abstract_methods
                            if method_is_abstract != abstract:
                                continue
                            method_is_virtual = (
                                name in virtual_methods or name in overridden_methods
                            )
                            if not abstract and method_is_virtual != virtual:
                                continue
                        elif typ == "attribute":
                            if signal and not isinstance(chobj, _pyqtSignal):
                                continue
                            if not signal and isinstance(chobj, _pyqtSignal):
                                continue
                            # skip monkey patched enums
                            # the monkeypatched enums coming out of scoped enum inherit Enum
                            # while the standard/old ones do not
                            if hasattr(chobj, "__objclass__") and issubclass(
                                chobj.__objclass__, Enum
                            ):
                                continue
                        elif typ == "class":
                            if enum:
                                if not issubclass(chobj, Enum):
                                    continue
                            if not enum and issubclass(chobj, Enum):
                                continue
                            # skip type aliases (e.g. QgsFeatureRequest.Flags
                            # is an alias for Qgis.FeatureRequestFlags)
                            if hasattr(
                                chobj, "__qualname__"
                            ) and not chobj.__qualname__.startswith(f"{obj.__name__}."):
                                continue
                        items.append(name)
                except AttributeError:
                    continue
            public = [x for x in items if x in include_public or not x.startswith("_")]
            return public, items
        except BaseException as e:
            print(str(e))
            raise e

    def import_by_name(
        self,
        name: str,
        prefixes: list[str | None],
    ) -> tuple[str, Any, Any, str]:
        """
        We have to wrap the original import_by_name, which raises noisy
        exceptions when trying to handle class attributes exposed by SIP.
        """
        try:
            res = super().import_by_name(name, prefixes)
        except ImportExceptionGroup:
            # class attribute import failed, just handle this by faking
            # the results. The resultant documentation still correctly
            # contains the attribute docstrings...
            name_parts = name.split(".")
            parent_name = ".".join(name_parts[:-1])
            parent_res = super().import_by_name(parent_name, prefixes)
            res = (name, None, parent_res[2], parent_res[3])

        return res

    def run(self):
        clazz = self.arguments[0]
        rubric_title = None
        rubric_description = None
        rubric_elems = None
        rubric_public_elems = None
        try:
            (module_name, class_name) = clazz.rsplit(".", 1)
            m = __import__(module_name, globals(), locals(), [class_name])
            c = getattr(m, class_name)
            if "abstract_methods" in self.options:
                rubric_title = "Abstract Methods"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "method", self.options, ["__init__"], abstract=True
                )
            elif "methods" in self.options:
                rubric_title = "Methods"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "method", self.options, ["__init__"]
                )
            elif "virtual_methods" in self.options:
                rubric_title = "Virtual Methods"
                rubric_description = f"In PyQGIS, **only** methods marked as ``virtual`` can be safely overridden in a Python subclass of {class_name}. See the `FAQ <../faq.html#what-are-virtual-methods>`_ for more details."
                _, rubric_elems = self.get_members(
                    self.state.document, c, "method", self.options, ["__init__"], virtual=True
                )
            elif "static_methods" in self.options:
                rubric_title = "Static Methods"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "method", self.options, static=True
                )
            elif "classes" in self.options:
                rubric_title = "Classes"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "class", self.options, None, False, False
                )
            elif "enums" in self.options:
                rubric_title = "Enums"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "class", self.options, None, False, True
                )
            elif "signals" in self.options:
                rubric_title = "Signals"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "attribute", self.options, None, signal=True
                )
            elif "attributes" in self.options:
                rubric_title = "Attributes"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "attribute", self.options, None, False
                )

            if rubric_elems:
                rubric_public_elems = list(filter(lambda e: not e.startswith("_"), rubric_elems))
                self.content = [f"~{clazz}.{elem}" for elem in rubric_public_elems]
        except BaseException as e:
            print(str(e))
            raise e
        finally:
            # add the title and descriptions before the return of the run
            ret = super().run()
            if rubric_description:
                if rubric_public_elems and len(rubric_public_elems) > 0:
                    settings = OptionParser(components=(Parser,)).get_default_values()
                    document = new_document("", settings)

                    # Parse the RST content
                    parser = Parser()
                    parser.parse(rubric_description, document)

                    # Extract the content from the parsed document
                    rst_nodes = document.children

                    # Insert the RST nodes into your document
                    for node in rst_nodes:
                        ret.insert(0, node)
            if rubric_title:
                if rubric_public_elems and len(rubric_public_elems) > 0:
                    rub = nodes.rubric("", rubric_title)
                    ret.insert(0, rub)
                else:
                    ret = []
            return ret
