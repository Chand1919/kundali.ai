# src/__init__.py
"""
Package initializer for the welfare eligibility project.
This file ensures DB initialization when src is imported.
"""
from .utils import init_db

# initialize DB on import
init_db()
