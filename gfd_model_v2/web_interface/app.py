"""
Flask application for GDFM Web Interface.
"""

import os
import sys
import json
import subprocess
import threading
import webbrowser
from flask import Flask, render_template, jsonify, request

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_app():
    """Create and configure the Flask application."""
    # Get the directory where app.py is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config['SECRET_KEY'] = 'gdfm-web-interface-secret'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for static files
    app.jinja_env.auto_reload = True
    
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    @app.route('/')
    def index():
        """Render the main interface."""
        return render_template('index.html')
    
    @app.route('/api/files')
    def get_files():
        """Get the project file tree structure."""
        def build_tree(path, depth=0, max_depth=5):
            """Recursively build file tree."""
            if depth > max_depth:
                return None
            
            name = os.path.basename(path)
            
            # Skip hidden files and __pycache__
            if name.startswith('.') or name == '__pycache__':
                return None
            
            node = {
                'name': name,
                'path': os.path.relpath(path, project_root).replace('\\', '/'),
                'type': 'directory' if os.path.isdir(path) else 'file'
            }
            
            if os.path.isdir(path):
                children = []
                try:
                    items = sorted(os.listdir(path))
                    # Directories first, then files
                    dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
                    files = [i for i in items if os.path.isfile(os.path.join(path, i))]
                    
                    for item in dirs + files:
                        child_path = os.path.join(path, item)
                        child_node = build_tree(child_path, depth + 1)
                        if child_node:
                            # Only include directories that have .py files
                            if child_node['type'] == 'directory':
                                if child_node.get('children') or has_python_files(child_path):
                                    children.append(child_node)
                            elif item.endswith('.py'):
                                children.append(child_node)
                except PermissionError:
                    pass
                
                node['children'] = children
            
            return node
        
        def has_python_files(path):
            """Check if directory contains Python files."""
            try:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if item.endswith('.py'):
                        return True
                    if os.path.isdir(full_path) and not item.startswith('.') and item != '__pycache__':
                        if has_python_files(full_path):
                            return True
            except PermissionError:
                pass
            return False
        
        tree = build_tree(project_root)
        return jsonify(tree)
    
    @app.route('/api/file/<path:filepath>')
    def get_file(filepath):
        """Get file contents."""
        full_path = os.path.join(project_root, filepath)
        
        if not os.path.exists(full_path):
            return jsonify({'error': 'File not found'}), 404
        
        if not os.path.isfile(full_path):
            return jsonify({'error': 'Not a file'}), 400
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'path': filepath,
                'name': os.path.basename(filepath),
                'content': content
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/file/<path:filepath>', methods=['PUT'])
    def save_file(filepath):
        """Save file contents."""
        full_path = os.path.join(project_root, filepath)
        
        # Security check: ensure path is within project
        real_path = os.path.realpath(full_path)
        real_root = os.path.realpath(project_root)
        if not real_path.startswith(real_root):
            return jsonify({'error': 'Access denied'}), 403
        
        if not os.path.exists(full_path):
            return jsonify({'error': 'File not found'}), 404
        
        if not os.path.isfile(full_path):
            return jsonify({'error': 'Not a file'}), 400
        
        if not filepath.endswith('.py'):
            return jsonify({'error': 'Can only edit Python files'}), 400
        
        data = request.get_json()
        content = data.get('content')
        
        if content is None:
            return jsonify({'error': 'No content provided'}), 400
        
        try:
            with open(full_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            return jsonify({
                'success': True,
                'path': filepath,
                'message': 'File saved successfully'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/run', methods=['POST'])
    def run_file():
        """Run a Python file and return output."""
        data = request.get_json()
        filepath = data.get('path')
        
        if not filepath:
            return jsonify({'error': 'No file path provided'}), 400
        
        full_path = os.path.join(project_root, filepath)
        
        if not os.path.exists(full_path):
            return jsonify({'error': 'File not found'}), 404
        
        if not filepath.endswith('.py'):
            return jsonify({'error': 'Can only run Python files'}), 400
        
        # Detect framework type by inspecting imports
        framework_type = detect_framework_type(full_path)
        
        try:
            # Set environment to disable colors and add project to Python path
            env = os.environ.copy()
            env['NO_COLOR'] = '1'
            env['TERM'] = 'dumb'
            
            # Run with explicit sys.path insertion using runpy for proper module execution
            # Use forward slashes which work on Windows and avoid escaping issues
            safe_project_root = project_root.replace('\\', '/')
            safe_full_path = full_path.replace('\\', '/')
            wrapper_code = f'import sys; sys.path.insert(0, "{safe_project_root}"); import runpy; runpy.run_path("{safe_full_path}", run_name="__main__")'
            
            result = subprocess.run(
                [sys.executable, '-c', wrapper_code],
                capture_output=True,
                text=True,
                cwd=project_root,
                timeout=120,
                env=env
            )
            
            return jsonify({
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'framework': framework_type
            })
        except subprocess.TimeoutExpired:
            return jsonify({'error': 'Execution timed out after 2 minutes'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def detect_framework_type(filepath):
        """
        Detect which test framework a file uses by inspecting its imports.
        
        Returns:
            'v2' - New framework (imports from gfd_model_v2.framework)
            'v1' - Legacy framework (imports from base or GFDTest)
            'script' - Plain Python script (no test framework)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for new framework imports
            new_framework_patterns = [
                'from gfd_model_v2.framework import',
                'from framework import',
                'import gfd_model_v2.framework',
            ]
            for pattern in new_framework_patterns:
                if pattern in content:
                    return 'v2'
            
            # Check for legacy framework imports
            legacy_patterns = [
                'from base import',
                'from gfd_model_v2.base import',
                'class GFDTest',
                'GFDTest)',  # Inheriting from GFDTest
            ]
            for pattern in legacy_patterns:
                if pattern in content:
                    return 'v1'
            
            # No recognized test framework
            return 'script'
            
        except Exception:
            return 'script'
    
    @app.route('/api/stats')
    def get_stats():
        """Get project statistics."""
        stats = {
            'total_tests': 0,
            'categories': []
        }
        
        # Count test files
        gfd_model_path = os.path.join(project_root, 'gfd_model_v2')
        
        categories = [
            {'name': 'Engine Core Geometry', 'path': 'engine/core_geometry'},
            {'name': 'Traversal Engine', 'path': 'engine/traversal_engine'},
            {'name': 'Timing Analysis', 'path': 'engine/timing_analysis'},
            {'name': 'Information Theory', 'path': 'engine/information_theory'},
            {'name': 'Emergent Constants', 'path': 'calculations/emergent_constants'},
            {'name': 'Stellar Mechanics', 'path': 'calculations/stellar_mechanics'},
            {'name': 'Particle Physics', 'path': 'calculations/particle_physics'},
            {'name': 'Historical Systems', 'path': 'calculations/historical_systems'},
        ]
        
        for cat in categories:
            cat_path = os.path.join(gfd_model_path, cat['path'])
            count = 0
            if os.path.exists(cat_path):
                for f in os.listdir(cat_path):
                    if f.startswith('test_') and f.endswith('.py'):
                        count += 1
            stats['categories'].append({
                'name': cat['name'],
                'count': count
            })
            stats['total_tests'] += count
        
        return jsonify(stats)
    
    return app


def run_server(port=5000, open_browser=True):
    """Run the Flask development server."""
    app = create_app()
    
    if open_browser:
        # Open browser after short delay to let server start
        def open_browser_delayed():
            import time
            time.sleep(1)
            webbrowser.open(f'http://localhost:{port}')
        
        threading.Thread(target=open_browser_delayed, daemon=True).start()
    
    print(f"Starting GDFM Web Interface at http://localhost:{port}")
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='GFD Model Web Interface')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    args = parser.parse_args()
    run_server(port=args.port, open_browser=not args.no_browser)
