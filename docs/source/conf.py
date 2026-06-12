# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
project = "eRMSF"
copyright = "2025, Pablo Arantes"
author = "Pablo Arantes"

try:
    from importlib.metadata import version as get_version
    release = get_version("ermsfkit")
    version = ".".join(release.split(".")[:2])
except Exception:
    version = "0.1"
    release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.extlinks",
    "sphinx_copybutton",
    "myst_parser",
]

autosummary_generate = True
autodoc_mock_imports = ["MDAnalysis", "numpy"]
autodoc_member_order = "bysource"
autodoc_typehints = "description"

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = True
napoleon_use_ivar = True
napoleon_use_rtype = True

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]
htmlhelp_basename = "ermsfkitdoc"

latex_elements = {}
latex_documents = [
    (master_doc, "ermsfkit.tex", "eRMSF Documentation", "Pablo Arantes", "manual"),
]
man_pages = [
    (master_doc, "ermsfkit", "eRMSF Documentation", [author], 1)
]
texinfo_documents = [
    (master_doc, "ermsfkit", "eRMSF Documentation", author, "ermsfkit",
     "A Python Package for Ensemble RMSF Analysis of Molecular Dynamics and Structural Ensembles",
     "Scientific Computing"),
]

# -- Extension configuration -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "mdanalysis": ("https://docs.mdanalysis.org/stable/", None),
}

copybutton_prompt_text = r">>> |\\.\\.\\. |\\$ "
copybutton_prompt_is_regexp = True
