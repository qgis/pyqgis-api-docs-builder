# creates methods summary
# see https://stackoverflow.com/questions/20569011/python-sphinx-autosummary-automated-listing-of-member-functions
# added toctree and nosignatures in options

import re
from enum import Enum
from typing import Any

import PyQt5
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.ext import autosummary
from sphinx.ext.autodoc import MethodDocumenter
from sphinx.ext.autosummary import Autosummary, ImportExceptionGroup
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.inspect import isstaticmethod, safe_getattr

from documenters import OverloadedPythonMethodDocumenter

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

old_get_documenter = autosummary.get_documenter


def new_get_documenter(app, obj: Any, parent: Any):
    res = old_get_documenter(app, obj, parent)
    if issubclass(res, OverloadedPythonMethodDocumenter):
        # sorry, gross hack! OverloadedPythonMethodDocumenter works well
        # for generating the actual docs, but fails when we are building
        # the table of contents. So fallback to original class instead...
        return MethodDocumenter
    return res


autosummary.get_documenter = new_get_documenter


class AutoAutoSummary(Autosummary):
    """
    Create a summary for methods, attributes and signals (autosummary).

    If the summary contains elements, a title (Methods, Attributes or Signals)
    is automatically added before (using the rubric directive).

    see https://stackoverflow.com/questions/20569011/python-sphinx-autosummary-automated-listing-of-member-functions
    """

    option_spec = {
        "methods": directives.unchanged,
        "static_methods": directives.unchanged,
        "signals": directives.unchanged,
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
                    documenter = autosummary.get_documenter(doc.settings.env.app, chobj, obj)
                    # cl = get_class_that_defined_method(chobj)
                    # print(name, chobj.__qualname__, type(chobj), issubclass(chobj, Enum), documenter.objtype)
                    if documenter.objtype == typ:
                        skipped = AutoAutoSummary.skip_member(
                            doc, chobj, name, options, documenter.objtype
                        )
                        if skipped is True:
                            continue
                        if typ == "method":
                            method_is_static = isstaticmethod(chobj, obj, name)
                            if method_is_static != static:
                                continue
                        elif typ == "attribute":
                            if signal and not isinstance(chobj, PyQt5.QtCore.pyqtSignal):
                                continue
                            if not signal and isinstance(chobj, PyQt5.QtCore.pyqtSignal):
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
        rubric_elems = None
        rubric_public_elems = None
        try:
            (module_name, class_name) = clazz.rsplit(".", 1)
            m = __import__(module_name, globals(), locals(), [class_name])
            c = getattr(m, class_name)
            if "methods" in self.options:
                rubric_title = "Methods"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "method", self.options, ["__init__"]
                )
            elif "static_methods" in self.options:
                rubric_title = "Static Methods"
                _, rubric_elems = self.get_members(
                    self.state.document, c, "method", self.options, static=True
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
            # add the title before the return of the run
            ret = super().run()
            if rubric_title:
                if rubric_public_elems and len(rubric_public_elems) > 0:
                    rub = nodes.rubric("", rubric_title)
                    ret.insert(0, rub)
            return ret
