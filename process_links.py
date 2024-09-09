# This scripts provides formatting for signature and docstrings to create links
# Links are not rendered in signatures: https://github.com/sphinx-doc/sphinx/issues/1059
# Also, sadly we cannot use existing extension autodoc-auto-typehints
# since __annotations__ are not filled in QGIS API, obviously because of SIP
#
# This logic has been copied from the existing extension with some tuning for PyQGIS

import enum
import inspect
import re

import yaml

with open("pyqgis_conf.yml") as f:
    cfg = yaml.safe_load(f)

from sphinx.ext.autodoc import AttributeDocumenter, Documenter, MethodDocumenter

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

parent_obj = None


def new_attribute_get_doc(self):
    # we need to make self.parent accessible to process_docstring -- this
    # is a hacky approach to store it temporarily in a global. Sorry!
    global parent_obj
    try:
        if self.object_name in self.parent.__attribute_docs__:
            parent_obj = self.parent
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


# https://github.com/sphinx-doc/sphinx/blob/685e3fdb49c42b464e09ec955e1033e2a8729fff/sphinx/ext/autodoc/__init__.py#L51
# adapted to handle signals

# https://regex101.com/r/lSB3rK/2/
py_ext_sig_re = re.compile(
    r"""^ ([\w.]+::)?            # explicit module name
          ([\w.]+\.)?            # module and/or class name(s)
          (\w+)  \s*             # thing name
          (?: \((.*)\)          # optional: arguments
          (?:\s* -> \s* ([\w.]+(?:\[.*?\])?))?   # return annotation
          (?:\s* \[(signal)\])?    # is signal
          )? $                   # and nothing more
          """,
    re.VERBOSE,
)


def create_links(doc: str) -> str:
    # fix inheritance
    doc = re.sub(r"qgis\._(core|gui|analysis|processing)\.", r"", doc)
    # class
    doc = re.sub(r"\b(Qgi?s[A-Z]\w+)([, )]|\. )", r":py:class:`.\1`\2", doc)
    return doc


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
            lines_out = []
            # loop through remaining lines, which are the constructors. Format
            # these up so they look like proper __init__ method documentation
            for i, line in enumerate(lines):
                if re.match(rf"^{class_name}\(", line):
                    lines_out.append(
                        re.sub(rf"\b{class_name}\(", ".. py:method:: __init__(", line)
                    )
                    lines_out.append("    :noindex:")
                    lines_out.append("")
                else:
                    lines_out.append("    " + line)

            lines[:] = lines_out[:]
            return

    for i in range(len(lines)):
        # fix seealso
        # lines[i] = re.sub(r':py: func:`(\w+\(\))`', r':func:`.{}.\1()'.format(what), lines[i])
        lines[i] = create_links(lines[i])

    def inject_args(_args, _lines):
        for arg in _args:
            try:
                argname, hint = arg.split(": ")
            except ValueError:
                continue
            searchfor = f":param {argname}:"
            insert_index = None

            for i, line in enumerate(_lines):
                if line.startswith(searchfor):
                    insert_index = i
                    break

            if insert_index is None:
                _lines.append(searchfor)
                insert_index = len(_lines)

            if insert_index is not None:
                _lines.insert(insert_index, f":type {argname}: {create_links(hint)}")

    if what == "attribute":
        global parent_obj
        try:
            args = parent_obj.__signal_arguments__.get(name.split(".")[-1], [])
            inject_args(args, lines)
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
            match = py_ext_sig_re.match(signature)
            if match:
                del lines[0]

        if match is None:
            signature = obj.__doc__.split("\n")[0]
            if signature == "":
                return
            match = py_ext_sig_re.match(signature)

        if match is None:
            if name not in cfg["non-instantiable"]:
                raise Warning(f"invalid signature for {name}: {signature}")

        else:
            exmod, path, base, args, retann, signal = match.groups()

            if args:
                args = args.split(", ")
                inject_args(args, lines)

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

                    lines.insert(insert_index, f":rtype: {create_links(retann)}")


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


class OverloadedPythonMethodDocumenter(MethodDocumenter):
    objtype = "method"
    priority = MethodDocumenter.priority

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        return MethodDocumenter.can_document_member(member, membername, isattr, parent)

    @staticmethod
    def parse_signatures(docstring):
        """
        Extracts each signature from a sip generated docstring
        """
        signature_pattern = r"(\w+\(.*?\))(?:\s*->\s*\(?\w+(?:,\s*\w+)*\)?)?"
        res = []
        current_signature_docs = []
        for line in docstring.split("\n"):

            if re.match(signature_pattern, line):
                if current_signature_docs:
                    res.append(current_signature_docs)

                # Extract just the parameter part of each signature
                params = re.search(r"\((.*?)\)", line).group()
                current_signature_docs = [params]
            else:
                current_signature_docs += [line]
        if current_signature_docs:
            res.append(current_signature_docs)

        return res

    def parse_signature_blocks(self, docstring):
        """
        Extracts each signature from a sip generated docstring, and
        returns each signature in a tuple with the docs for just
        that signature.
        """
        res = []
        current_sig = ""
        current_desc = ""
        for line in docstring.split("\n"):
            match = re.match(
                r"^\s*\w+(\([^)]*\)(?:\s*->\s*[^:\n]+)?)\s*((?:(?!\w+\().)*)\s*$", line
            )
            if match:
                if current_sig:
                    res.append((current_sig, current_desc))
                current_sig = match.group(1)
                current_desc = match.group(2)
                if current_desc:
                    current_desc += "\n"
            else:
                current_desc += line + "\n"

        if current_sig:
            res.append((current_sig, current_desc))

        return res

    def add_content(self, more_content):
        """
        Parse the docstring to get all signatures and their descriptions
        """
        sourcename = self.get_sourcename()
        docstring = inspect.getdoc(self.object)
        if docstring:
            # does this method have multiple overrides?
            signature_blocks = self.parse_signature_blocks(docstring)

            if len(signature_blocks) <= 1:
                # nope, just use standard formatter then!
                super().add_content(more_content)
                return

            # add a method output for EVERY override
            for i, (signature, description) in enumerate(signature_blocks):
                # this pattern is used in the autodoc source!
                old_indent = self.indent
                new_indent = (
                    " "
                    * len(self.content_indent)
                    * (len(self.indent) // len(self.content_indent) - 1)
                )
                self.indent = new_indent
                # skip this class, go straight to super. The add_directive_header
                # implementation from this class will omit the signatures of
                # overridden methods
                super().add_directive_header(signature)
                self.indent = old_indent

                if i > 0:
                    # we can only index the first signature!
                    self.add_line(":no-index:", sourcename)

                self.add_line("", sourcename)

                doc_for_this_override = self.object_name + signature + "\n" + description
                for line in self.process_doc([doc_for_this_override.split("\n")]):
                    self.add_line(line, sourcename)

    def add_directive_header(self, sig):
        # Parse the docstring to get all signatures
        docstring = inspect.getdoc(self.object)
        if docstring:
            signatures = self.parse_signatures(docstring)
        else:
            signatures = [sig]  # Use the original signature if no docstring

        if len(signatures) > 1:
            # skip overridden method directive headers here, we will generate
            # them later when we pass the actual docstring
            return

        return super().add_directive_header(sig)
