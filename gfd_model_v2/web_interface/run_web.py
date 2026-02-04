#!/usr/bin/env python
"""
Standalone launcher for GDFM Web Interface.

Usage:
    python run_web.py [--port PORT] [--no-browser]

This starts the Flask development server and opens the web interface
in your default browser.
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import run_server


def main():
    parser = argparse.ArgumentParser(description='GDFM Web Interface')
    parser.add_argument('--port', type=int, default=5000, help='Port to run server on (default: 5000)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║          GDFM Web Interface                           ║
    ║          Gravity Field Dynamics Model                 ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Starting server at http://localhost:{:<5}            ║
    ║  Press Ctrl+C to stop                                 ║
    ╚═══════════════════════════════════════════════════════╝
    """.format(args.port))
    
    run_server(port=args.port, open_browser=not args.no_browser)


if __name__ == '__main__':
    main()
