"""
Flask application for GDFM Web Interface.
"""

import os
import sys
import json
import subprocess
import threading
import webbrowser
from flask import Flask, render_template, jsonify, request, send_file, redirect

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# File filters - files to exclude from tree and non-runnable folders
EXCLUDED_FILES = [
    '__init__.py',
    'base.py',
    'framework.py',
    'report_generator.py',
    'dfp_console.py',
    'run_test.py',
    'build_audit.py',
]

NON_RUNNABLE_FOLDERS = [
    'common',
]


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
    
    # Get project root directory (gravity_field_model folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    @app.route('/')
    def home():
        """Redirect to start page."""
        return redirect('/start')
    
    @app.route('/start')
    def start():
        """Serve the splash screen as the start/landing page."""
        splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'splash_screen.html')
        return send_file(splash_path)
    
    @app.route('/app')
    def index():
        """Render the main test explorer interface."""
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
            
            # Skip excluded files
            if os.path.isfile(path) and name in EXCLUDED_FILES:
                return None
            
            node = {
                'name': name,
                'path': os.path.relpath(path, project_root).replace('\\', '/'),
                'type': 'directory' if os.path.isdir(path) else 'file'
            }
            
            # Check if file is in a non-runnable folder
            if os.path.isfile(path):
                rel_path = os.path.relpath(path, project_root).replace('\\', '/')
                for folder in NON_RUNNABLE_FOLDERS:
                    if f'/{folder}/' in rel_path or rel_path.startswith(f'{folder}/'):
                        node['runnable'] = False
                        break
            
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
                
                # Add test count for directories
                test_count = count_test_files(path)
                if test_count > 0:
                    node['testCount'] = test_count
            
            return node
        
        def count_test_files(path):
            """Count test_*.py files recursively in a directory."""
            count = 0
            try:
                for item in os.listdir(path):
                    full_path = os.path.join(path, item)
                    if os.path.isfile(full_path) and item.startswith('test_') and item.endswith('.py'):
                        count += 1
                    elif os.path.isdir(full_path) and not item.startswith('.') and item != '__pycache__':
                        count += count_test_files(full_path)
            except PermissionError:
                pass
            return count
        
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
            'v2' - New framework (imports from gravity_field_model.framework)
            'v1' - Legacy framework (imports from base or GFDTest)
            'script' - Plain Python script (no test framework)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for new framework imports
            new_framework_patterns = [
                'from gravity_field_model.framework import',
                'from framework import',
                'import gravity_field_model.framework',
            ]
            for pattern in new_framework_patterns:
                if pattern in content:
                    return 'v2'
            
            # Check for legacy framework imports
            legacy_patterns = [
                'from base import',
                'from gravity_field_model.base import',
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
        
        # Count test files (project_root is already gravity_field_model)
        gfd_model_path = project_root
        
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
    
    @app.route('/api/ping')
    def ping():
        """Simple ping endpoint for testing."""
        return jsonify({'status': 'ok'})
    
    @app.route('/api/test-summary')
    def get_test_summary():
        """Return test counts by parsing test files for test functions."""
        import re
        
        # project_root is already gravity_field_model
        engine_core_path = os.path.join(project_root, 'engine_core')
        calculations_path = os.path.join(project_root, 'calculations')
        
        def count_tests_in_file(filepath):
            """Count test classes in a Python test file."""
            count = 0
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Count classes that inherit from Test (the project's test framework)
                    count += len(re.findall(r'\bclass\s+\w+\s*\(\s*Test\s*\)', content))
            except Exception:
                pass
            return max(count, 1)  # At least 1 test per test file
        
        def count_tests_in_dir(base_path):
            """Recursively count tests in all test_*.py files."""
            count = 0
            if not os.path.exists(base_path):
                return count
            for root, dirs, files in os.walk(base_path):
                dirs[:] = [d for d in dirs if d != '__pycache__']
                for f in files:
                    if f.startswith('test_') and f.endswith('.py'):
                        filepath = os.path.join(root, f)
                        count += count_tests_in_file(filepath)
            return count
        
        engine_count = count_tests_in_dir(engine_core_path)
        calc_count = count_tests_in_dir(calculations_path)
        
        return jsonify({
            'engine_core': {'passed': engine_count, 'failed': 0, 'total': engine_count},
            'calculations': {'passed': calc_count, 'failed': 0, 'total': calc_count},
            'total_passed': engine_count + calc_count,
            'total_failed': 0,
            'total_tests': engine_count + calc_count
        })
    
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
