"""Sphinx configuration for the Orange County Lettings documentation."""
import os
import sys
from pathlib import Path

import django


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
django.setup()

project = 'Orange County Lettings'
author = 'Orange County Lettings'
language = 'fr'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

autodoc_member_order = 'bysource'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
root_doc = 'index'
