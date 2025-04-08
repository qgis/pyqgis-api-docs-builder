# This scripts provides formatting for signature and docstrings to create links
# Links are not rendered in signatures: https://github.com/sphinx-doc/sphinx/issues/1059
# Also, sadly we cannot use existing extension autodoc-auto-typehints
# since __annotations__ are not filled in QGIS API, obviously because of SIP
#
# This logic has been copied from the existing extension with some tuning for PyQGIS


from sphinx.ext.autodoc import AttributeDocumenter, Documenter

from docs_builder.autodoc import AutoDocAdditions

old_get_doc = Documenter.get_doc


def new_get_doc(self) -> list[list[str]] | None:
    try:
        if self.object_name in self.parent.__attribute_docs__:
            docs = self.parent.__attribute_docs__[self.object_name]
            return [docs.split("\n")]
    except AttributeError:
        pass

    return old_get_doc(self)


Documenter.get_doc = new_get_doc

old_attribute_get_doc = AttributeDocumenter.get_doc


def new_attribute_get_doc(self):
    # we need to make self.parent accessible to process_docstring -- this
    # is a hacky approach to store it temporarily in a global. Sorry!
    try:
        if self.object_name in self.parent.__attribute_docs__:
            AutoDocAdditions.PARENT_OBJ = self.parent
            docs = self.parent.__attribute_docs__[self.object_name]
            return [docs.split("\n")]
    except AttributeError:
        pass

    return old_attribute_get_doc(self)


AttributeDocumenter.get_doc = new_attribute_get_doc

old_format_signature = Documenter.format_signature


def new_format_signature(self, **kwargs) -> str:
    """
    Monkey patch signature formatting to retrieve signature for
    signals, which are actually attributes and so don't have a real
    signature available!
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

    return old_format_signature(self, **kwargs)


Documenter.format_signature = new_format_signature


def process_signature(app, what, name, obj, options, signature, return_annotation):
    # we cannot render links in signature for the moment, so do nothing
    # https://github.com/sphinx-doc/sphinx/issues/1059
    return signature, return_annotation


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


def process_bases(app, name, obj, option, bases: list) -> None:
    """Here we fine tune how the base class's classes are displayed."""
    for i, base in enumerate(bases):
        # replace 'sip.wrapper' base class with 'object'
        if base.__name__ == "wrapper":
            bases[i] = object
