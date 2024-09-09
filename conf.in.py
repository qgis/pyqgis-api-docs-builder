import os
import sys

import sphinx_rtd_theme
import yaml

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath("../../"))

with open("../../pyqgis_conf.yml") as f:
    cfg = yaml.safe_load(f)


# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinxcontrib.jquery",
    "sphinx.ext.linkcode",
    "inheritance_diagram",
    "sphinx.ext.graphviz",
]  # , 'rinoh.frontend.sphinx'], 'sphinx_autodoc_typehints'

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "QGIS Python API"
copyright = "2018, QGIS project"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "__QGIS_VERSION__"
# The full version, including alpha/beta/rc tags.
release = "__QGIS_VERSION__"

if version == "master":
    QGIS_GIT_TAG = "master"
else:
    QGIS_GIT_TAG = f"release-{release.replace('.', '_')}"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["output", "i18n", "resources", "scripts"]

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]  # use with module import

# html_theme_path = ['.']  # use with git submodule

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "collapse_navigation": False,
    "sticky_navigation": False,
    "display_version": True,
    "prev_next_buttons_location": None,
    "titles_only": True,
    "versioning": True,
    "canonical_url": "https://qgis.org/pyqgis/latest",
    "navigation_depth": 1,
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = ""

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "../../resources/en/common/logo.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "../../resources/en/common/qgis.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['themes/qgis-theme/static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%H:%M %b %d, %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

current_stable = str(cfg["current_stable"])
current_ltr = str(cfg["current_ltr"])
version_list = ("master", current_stable, current_ltr)

graphviz_output_format = "svg"

url = cfg["pyqgis_url"]
if not url.endswith("/"):
    url += "/"

if version not in version_list:
    raise ValueError("QGIS version is not in version list", version, version_list)

context = {
    # 'READTHEDOCS': True,
    "version_downloads": False,
    "current_version": version,
    "version": version,
    "versions": [[v, url + v] for v in ("master", cfg["current_stable"], cfg["current_ltr"])],
    "version_branch": (
        "".join(["release-", version]).replace(".", "_") if version != "master" else "master"
    ),
    "display_lower_left": True,
    # 'downloads': [ ['PDF', '/builders.pdf'], ['HTML', '/builders.tgz'] ],
}

html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

if "html_context" in globals():
    html_context.update(context)  # noqa: F821
else:
    html_context = context

templates_path = ["_templates"]

autodoc_default_options = {"show-inheritance": True}

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# It would be nice to show link to source: https://github.com/qgis/pyqgis/issues/37
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = "QGISAPIDOC"

rst_prolog = """
.. role:: disclaimer
.. |updatedisclaimer| replace:: :disclaimer:`Docs for 'QGIS __QGIS_VERSION__'`
"""

# Substitutions icons below are sorted
# NOTE that for inline images (like button and menu icons inline in text) you HAVE TO make a substitution
# so ONLY use common for this kind of images
rst_epilog = """
.. |localCRS| replace:: :kbd:`WGS 84 / UTM 34S`
"""

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "qgiswebsite", "QGIS Website Documentation", ["QGIS Contributors"], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False

locale_dirs = ["../i18n/"]
gettext_compact = False

class_maps = {}
for module in ("3d", "analysis", "core", "gui", "server"):
    with open(f"/usr/lib/python3/dist-packages/qgis/{module}/class_map.yaml") as f:
        class_maps[module] = yaml.safe_load(f)


def linkcode_resolve(domain, info):
    if domain != "py":
        return None
    if not info["module"]:
        return None
    try:
        module = info["module"].split(".")[1]
    except IndexError:
        return None
    if module == "_3d":
        module = "3d"
    try:
        header = class_maps[module][info["fullname"]]
        return f"https://github.com/qgis/QGIS/tree/{QGIS_GIT_TAG}/{header}"
    except KeyError:
        # class_name = info["fullname"].split(".")[0]
        # header = class_maps[module][class_name]
        # return f"https://github.com/qgis/QGIS/tree/{QGIS_GIT_TAG}/{header}"
        return None


def setup(app):
    try:
        from autoautosummary import AutoAutoSummary
        from process_links import (
            OverloadedPythonMethodDocumenter,
            process_bases,
            process_docstring,
            process_signature,
            skip_member,
        )

        app.add_directive("autoautosummary", AutoAutoSummary)
        app.add_autodocumenter(OverloadedPythonMethodDocumenter)
        app.connect("autodoc-process-signature", process_signature)
        app.connect("autodoc-process-docstring", process_docstring)
        app.connect("autodoc-skip-member", skip_member)
        app.connect("autodoc-process-bases", process_bases)
    except BaseException as e:
        raise e
