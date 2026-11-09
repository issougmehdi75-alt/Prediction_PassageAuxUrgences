
# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath('../..'))  # pour autodoc (package urgences)

# -- Project information -----------------------------------------------------
project = 'Prévision des Passages aux Urgences'
copyright = '2025–2026, Issoug El Mehdi & Bado Ange Yipene Cenacle'
author = 'Issoug El Mehdi & Bado Ange Yipene Cenacle'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = []
exclude_patterns = []
language = 'fr'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = []

html_theme_options = {
    'logo_only': False,
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'style_nav_header_background': '#0d2847',
}

html_title = "🏥 Prévision Urgences — Hôpital Mohamed V"

# Les dépendances lourdes ne sont pas installées sur Read the Docs : on les simule.
autodoc_mock_imports = ["pandas", "numpy", "plotly", "streamlit", "prophet", "sklearn", "statsmodels"]
autodoc_member_order = "bysource"
