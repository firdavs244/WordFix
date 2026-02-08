"""
Settings package.

Each settings module (development.py, test.py, production.py)
imports from base.py using `from .base import *`.
The DJANGO_SETTINGS_MODULE env var controls which module Django uses.

Do NOT auto-import here — it causes double-import issues.
"""
