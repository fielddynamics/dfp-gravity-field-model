#!/usr/bin/env python
"""
Launch the Gravity Field Model web application.

Usage:
    python run_app.py [--port PORT]

Example:
    python run_app.py
    python run_app.py --port 5001
"""

import argparse
import sys
import os

# Add the project root to the path so 'from gravity_field_model.xxx import yyy' works
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gravity_field_model.web_interface.app import run_server


def main():
    parser = argparse.ArgumentParser(description='Gravity Field Model Web App')
    parser.add_argument('--port', type=int, default=5000, help='Port to run server on (default: 5000)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    
    args = parser.parse_args()
    
    print("""
    +-------------------------------------------------------+
    |          Gravity Field Model                          |
    +-------------------------------------------------------+
    |  Starting server at http://localhost:{:<5}            |
    |  Press Ctrl+C to stop                                 |
    +-------------------------------------------------------+
    """.format(args.port))
    
    run_server(port=args.port, open_browser=not args.no_browser)


if __name__ == '__main__':
    main()
