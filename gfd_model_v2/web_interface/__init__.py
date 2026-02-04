"""
GDFM Web Interface
==================

Flask-based web interface for the Gravity Field Dynamics Model.
Provides a Claude Code style interface for browsing and running tests.
"""

from .app import create_app, run_server

__all__ = ['create_app', 'run_server']
