"""
File filtering constants for the GDFM Web Interface.

This module defines which files should be excluded from the file tree
and which folders contain non-runnable files.
"""

# Files to completely exclude from the file tree
EXCLUDED_FILES = [
    '__init__.py',
    'base.py',
    'framework.py',
    'report_generator.py',
    'dfp_console.py',
    'run_test.py',
    'build_audit.py',
]

# Folders where files are viewable but not runnable (no Run button)
NON_RUNNABLE_FOLDERS = [
    'common',
]
