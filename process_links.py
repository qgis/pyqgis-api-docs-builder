# This scripts provides formatting for signature and docstrings to create links
# Links are not rendered in signatures: https://github.com/sphinx-doc/sphinx/issues/1059
# Also, sadly we cannot use existing extension autodoc-auto-typehints
# since __annotations__ are not filled in QGIS API, obviously because of SIP
#
# This logic has been copied from the existing extension with some tuning for PyQGIS

import enum
import re

import yaml

with open("pyqgis_conf.yml") as f:
    cfg = yaml.safe_load(f)


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


def show_inheritance(obj):
    # handle inheritance printing to patch qgis._core with qgis.core
    # https://github.com/sphinx-doc/sphinx/blob/685e3fdb49c42b464e09ec955e1033e2a8729fff/sphinx/ext/autodoc/__init__.py#L1103-L1109
    if hasattr(obj, "__bases__") and len(obj.__bases__):
        bases = [
            b.__module__ in ("__builtin__", "builtins")
            and ":class:`%s`" % b.__name__
            or f":class:`{b.__module__}.{b.__name__}`"
            for b in obj.__bases__
        ]
        return "Bases: %s" % ", ".join(bases)
    return None


def create_links(doc: str) -> str:
    # fix inheritance
    doc = re.sub(r"qgis\._(core|gui|analysis|processing)\.", r"", doc)
    # class
    doc = re.sub(r"\b(Qgi?s[A-Z]\w+)([, )]|\. )", r":py:class:`.\1`\2", doc)
    return doc


def process_docstring(app, what, name, obj, options, lines):
    # print('d', what, name, obj, options)
    bases = show_inheritance(obj)
    if bases:
        lines.insert(0, "")
        lines.insert(0, bases)

    for i in range(len(lines)):

        # fix seealso
        # lines[i] = re.sub(r':py: func:`(\w+\(\))`', r':func:`.{}.\1()'.format(what), lines[i])
        lines[i] = create_links(lines[i])

    # add return type and param type
    if what != "class" and not isinstance(obj, enum.EnumMeta) and obj.__doc__:
        signature = obj.__doc__.split("\n")[0]
        if signature != "":
            match = py_ext_sig_re.match(signature)
            if not match:
                print(obj)
                if name not in cfg["non-instantiable"]:
                    raise Warning(f"invalid signature for {name}: {signature}")
            else:
                exmod, path, base, args, retann, signal = match.groups()

                if args:
                    args = args.split(", ")
                    for arg in args:
                        try:
                            argname, hint = arg.split(": ")
                        except ValueError:
                            continue
                        searchfor = f":param {argname}:"
                        insert_index = None

                        for i, line in enumerate(lines):
                            if line.startswith(searchfor):
                                insert_index = i
                                break

                        if insert_index is None:
                            lines.append(searchfor)
                            insert_index = len(lines)

                        if insert_index is not None:
                            lines.insert(insert_index, f":type {argname}: {create_links(hint)}")

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
        print(f"skipping monkey patched enum {name}")
        return True
    return skip
