/**
 * GDFM Web Interface - JavaScript Application
 */

// Global state
let currentFile = null;
let fileContent = '';
let originalContent = '';  // Track original content for change detection
let fileTreeData = null;  // Store the full tree data for filtering
let currentFilter = '';
let hasUnsavedChanges = false;
let initialTestsRun = false;  // Track if initial test run has happened

// Folders where files are viewable but not runnable
const NON_RUNNABLE_FOLDERS = ['common'];

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadFileTree();
    initResizeHandle();
    initCodeEditor();

    // Run all tests once on app load (non-blocking)
    if (!initialTestsRun) {
        initialTestsRun = true;
        runInitialTests();
    }
});

/**
 * Run all tests on initial page load
 */
async function runInitialTests() {
    const loadingDots = document.getElementById('test-loading');
    const resultsList = document.getElementById('results-list');
    const engineLine = document.getElementById('engine-line');
    const calcLine = document.getElementById('calc-line');
    const totalLine = document.getElementById('total-line');

    try {
        const response = await fetch('/api/test-summary');
        const data = await response.json();

        // Hide loading, show results
        if (loadingDots) loadingDots.style.display = 'none';
        if (resultsList) resultsList.style.display = 'block';

        // Format results inline
        if (engineLine) {
            engineLine.innerHTML = formatResultLine('Engine Core', data.engine_core.passed, data.engine_core.failed);
        }
        if (calcLine) {
            calcLine.innerHTML = formatResultLine('Calculations', data.calculations.passed, data.calculations.failed);
        }
        if (totalLine) {
            totalLine.innerHTML = formatResultLine('Total', data.total_passed, data.total_failed);
        }

    } catch (error) {
        console.error('Failed to run initial tests:', error);
        if (loadingDots) loadingDots.style.display = 'none';
    }
}

/**
 * Format a result line with label and pass/fail counts
 */
function formatResultLine(label, passed, failed) {
    if (failed === 0) {
        return `<span class="label">${label}:</span> <span class="passed">${passed} passed</span>`;
    } else {
        return `<span class="label">${label}:</span> <span class="passed">${passed} passed</span>, <span class="failed">${failed} failed</span>`;
    }
}

/**
 * Initialize the sidebar resize handle
 */
function initResizeHandle() {
    const resizeHandle = document.getElementById('resize-handle');
    const sidebar = document.querySelector('.sidebar');
    const appContainer = document.querySelector('.app-container');

    if (!resizeHandle || !sidebar) return;

    let isResizing = false;
    let startX = 0;
    let startWidth = 0;

    resizeHandle.addEventListener('mousedown', (e) => {
        isResizing = true;
        startX = e.clientX;
        startWidth = sidebar.offsetWidth;

        resizeHandle.classList.add('dragging');
        appContainer.classList.add('resizing');

        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;

        const deltaX = e.clientX - startX;
        const newWidth = Math.min(Math.max(startWidth + deltaX, 200), 600);

        sidebar.style.width = newWidth + 'px';
    });

    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;
            resizeHandle.classList.remove('dragging');
            appContainer.classList.remove('resizing');
        }
    });
}

/**
 * Initialize the code editor
 */
function initCodeEditor() {
    const editor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    const highlight = document.getElementById('code-highlight');
    const container = document.querySelector('.code-editor-container');

    if (!editor || !lineNumbers) return;

    // Sync scroll from container to line numbers
    if (container) {
        container.addEventListener('scroll', () => {
            lineNumbers.scrollTop = container.scrollTop;
        });
    }

    // Handle input changes
    editor.addEventListener('input', () => {
        updateHighlight();
        updateLineNumbers();
        checkForChanges();
    });

    // Track cursor position
    editor.addEventListener('keyup', updateCursorPosition);
    editor.addEventListener('click', updateCursorPosition);
    editor.addEventListener('focus', updateCursorPosition);

    // Handle tab key for indentation
    editor.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = editor.selectionStart;
            const end = editor.selectionEnd;
            const value = editor.value;

            // Insert 4 spaces
            editor.value = value.substring(0, start) + '    ' + value.substring(end);
            editor.selectionStart = editor.selectionEnd = start + 4;

            // Trigger input event for change detection
            editor.dispatchEvent(new Event('input'));
        }

        // Ctrl+S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            if (hasUnsavedChanges) {
                saveFile();
            }
        }
    });
}

/**
 * Update the syntax highlighted display
 */
function updateHighlight() {
    const editor = document.getElementById('code-editor');
    const highlightCode = document.getElementById('code-highlight-code');

    if (!editor || !highlightCode) return;

    highlightCode.innerHTML = highlightSyntax(editor.value);
}

/**
 * Update line numbers based on editor content
 */
function updateLineNumbers() {
    const editor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');

    if (!editor || !lineNumbers) return;

    const lines = editor.value.split('\n');
    lineNumbers.innerHTML = lines.map((_, i) => i + 1).join('<br>');
}

/**
 * Update cursor position display
 */
function updateCursorPosition() {
    const editor = document.getElementById('code-editor');
    const positionDisplay = document.getElementById('cursor-position');

    if (!editor || !positionDisplay) return;

    const value = editor.value;
    const selectionStart = editor.selectionStart;

    // Count lines and column
    const textBeforeCursor = value.substring(0, selectionStart);
    const lines = textBeforeCursor.split('\n');
    const lineNumber = lines.length;
    const columnNumber = lines[lines.length - 1].length + 1;

    positionDisplay.textContent = `Ln ${lineNumber}, Col ${columnNumber}`;
}

/**
 * Check for unsaved changes
 */
function checkForChanges() {
    const editor = document.getElementById('code-editor');
    const saveBtn = document.getElementById('save-btn');
    const statusText = document.getElementById('editor-status');

    if (!editor || !saveBtn || !statusText) return;

    hasUnsavedChanges = editor.value !== originalContent;

    if (hasUnsavedChanges) {
        saveBtn.disabled = false;
        saveBtn.classList.add('has-changes');
        statusText.textContent = 'Modified';
        statusText.className = 'status-text modified';
    } else {
        saveBtn.disabled = true;
        saveBtn.classList.remove('has-changes');
        statusText.textContent = 'Ready';
        statusText.className = 'status-text';
    }
}

/**
 * Save the current file
 */
async function saveFile() {
    if (!currentFile || !hasUnsavedChanges) return;

    const editor = document.getElementById('code-editor');
    const saveBtn = document.getElementById('save-btn');
    const statusText = document.getElementById('editor-status');

    if (!editor) return;

    // Disable button and show saving state
    saveBtn.disabled = true;
    statusText.textContent = 'Saving...';
    statusText.className = 'status-text';

    try {
        const response = await fetch(`/api/file/${currentFile}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: editor.value
            })
        });

        const data = await response.json();

        if (data.error) {
            statusText.textContent = 'Error: ' + data.error;
            statusText.className = 'status-text error';
            saveBtn.disabled = false;
            return;
        }

        // Update original content to current
        originalContent = editor.value;
        fileContent = editor.value;
        hasUnsavedChanges = false;

        // Show success
        statusText.textContent = 'Saved';
        statusText.className = 'status-text saved';
        saveBtn.classList.remove('has-changes');

        // Reset status after delay
        setTimeout(() => {
            if (!hasUnsavedChanges) {
                statusText.textContent = 'Ready';
                statusText.className = 'status-text';
            }
        }, 2000);

    } catch (error) {
        console.error('Error saving file:', error);
        statusText.textContent = 'Error saving file';
        statusText.className = 'status-text error';
        saveBtn.disabled = false;
    }
}

/**
 * Load and render the file tree
 */
async function loadFileTree() {
    const treeContainer = document.getElementById('file-tree');

    try {
        const response = await fetch('/api/files');
        const data = await response.json();

        // Store tree data for filtering
        fileTreeData = data;

        treeContainer.innerHTML = '';
        const fileCount = renderTreeNode(data, treeContainer, 0, currentFilter);
        updateFileCount(fileCount);
    } catch (error) {
        treeContainer.innerHTML = '<div class="loading">Error loading files</div>';
        console.error('Error loading file tree:', error);
    }
}

/**
 * Filter files based on search pattern
 */
function filterFiles(pattern) {
    currentFilter = pattern.toLowerCase().trim();

    if (!fileTreeData) return;

    const treeContainer = document.getElementById('file-tree');
    treeContainer.innerHTML = '';

    const fileCount = renderTreeNode(fileTreeData, treeContainer, 0, currentFilter);
    updateFileCount(fileCount);

    // Auto-expand directories when filtering
    if (currentFilter) {
        document.querySelectorAll('.tree-item.directory').forEach(item => {
            item.classList.add('expanded');
        });
    }
}

/**
 * Update the file count display
 */
function updateFileCount(count) {
    const countElement = document.getElementById('file-count');
    if (countElement) {
        countElement.textContent = count > 0 ? `${count} tests` : '';
    }
}

/**
 * Check if a file matches the filter pattern (wildcard support)
 */
function matchesFilter(filename, pattern) {
    if (!pattern) return true;

    // Convert wildcard pattern to regex
    // * matches any characters, ? matches single character
    const regexPattern = pattern
        .replace(/[.+^${}()|[\]\\]/g, '\\$&')  // Escape special regex chars
        .replace(/\*/g, '.*')                   // * -> .*
        .replace(/\?/g, '.');                   // ? -> .

    try {
        const regex = new RegExp(regexPattern, 'i');
        return regex.test(filename);
    } catch (e) {
        // If regex is invalid, fall back to simple includes
        return filename.toLowerCase().includes(pattern);
    }
}

/**
 * Check if a node or any of its children match the filter
 */
function nodeMatchesFilter(node, pattern) {
    if (!pattern) return true;

    if (node.type === 'file') {
        return matchesFilter(node.name, pattern);
    }

    // For directories, check if any children match
    if (node.children) {
        return node.children.some(child => nodeMatchesFilter(child, pattern));
    }

    return false;
}

/**
 * Render a tree node and its children
 * Returns the count of visible files
 */
function renderTreeNode(node, container, depth, filter = '') {
    if (!node || !node.name) return 0;

    // Check if this node or its children match the filter
    if (filter && !nodeMatchesFilter(node, filter)) {
        return 0;
    }

    const item = document.createElement('div');
    item.className = `tree-item ${node.type}`;
    item.style.paddingLeft = `${16 + depth * 16}px`;
    item.setAttribute('data-path', node.path || '');
    item.setAttribute('data-name', node.name);

    const icon = document.createElement('span');
    icon.className = 'icon';

    const name = document.createElement('span');
    name.className = 'tree-item-name';

    // Highlight matching text if filtering
    if (filter && node.type === 'file' && matchesFilter(node.name, filter)) {
        name.innerHTML = highlightMatch(node.name, filter);
    } else {
        name.textContent = node.name;
    }

    item.appendChild(icon);
    item.appendChild(name);

    // Add test count for directories
    if (node.type === 'directory' && node.testCount > 0) {
        const count = document.createElement('span');
        count.className = 'test-count';
        count.textContent = node.testCount;
        item.appendChild(count);
    }

    let fileCount = 0;

    if (node.type === 'directory') {
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            item.classList.toggle('expanded');
        });

        container.appendChild(item);

        if (node.children && node.children.length > 0) {
            const childContainer = document.createElement('div');
            childContainer.className = 'tree-children';

            node.children.forEach(child => {
                fileCount += renderTreeNode(child, childContainer, depth + 1, filter);
            });

            // Only add child container if it has visible children
            if (childContainer.children.length > 0) {
                container.appendChild(childContainer);

                // Auto-expand when filtering, at root level, or calculations folder
                if (filter || depth === 0 || (depth === 1 && node.name === 'calculations')) {
                    item.classList.add('expanded');
                }
            }
        }
    } else {
        item.addEventListener('click', (e) => {
            e.stopPropagation();

            // Remove selection from other items
            document.querySelectorAll('.tree-item.selected').forEach(el => {
                el.classList.remove('selected');
            });
            item.classList.add('selected');

            openFile(node.path);
        });

        fileCount = 1;

        container.appendChild(item);
    }

    return fileCount;
}

/**
 * Highlight matching text in filename
 */
function highlightMatch(text, pattern) {
    if (!pattern) return escapeHtml(text);

    // Convert wildcard pattern to find the matching portion
    const simplePattern = pattern.replace(/\*/g, '').replace(/\?/g, '');
    if (!simplePattern) return escapeHtml(text);

    const lowerText = text.toLowerCase();
    const lowerPattern = simplePattern.toLowerCase();
    const index = lowerText.indexOf(lowerPattern);

    if (index === -1) return escapeHtml(text);

    const before = text.substring(0, index);
    const match = text.substring(index, index + simplePattern.length);
    const after = text.substring(index + simplePattern.length);

    return `${escapeHtml(before)}<span class="highlight-match">${escapeHtml(match)}</span>${escapeHtml(after)}`;
}

/**
 * Open a file in the viewer
 */
async function openFile(filepath) {
    // Check for unsaved changes
    if (hasUnsavedChanges) {
        const confirmDiscard = confirm('You have unsaved changes. Discard them?');
        if (!confirmDiscard) return;
    }

    try {
        const response = await fetch(`/api/file/${filepath}`);
        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        currentFile = filepath;
        fileContent = data.content;
        originalContent = data.content;
        hasUnsavedChanges = false;

        // Hide welcome view, show file viewer
        document.getElementById('welcome-view').style.display = 'none';
        document.getElementById('output-viewer').style.display = 'none';
        document.getElementById('file-viewer').style.display = 'flex';

        // Update file name
        document.getElementById('current-file-name').textContent = data.name;

        // Check if file is runnable (not in non-runnable folders)
        const runBtn = document.querySelector('.run-btn');
        if (runBtn) {
            const isRunnable = !NON_RUNNABLE_FOLDERS.some(folder =>
                filepath.includes(`/${folder}/`) || filepath.includes(`\\${folder}\\`)
            );
            runBtn.style.display = isRunnable ? 'block' : 'none';
        }

        // Render code in editor
        renderCode(data.content);

        // Reset editor status
        const saveBtn = document.getElementById('save-btn');
        const statusText = document.getElementById('editor-status');
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.classList.remove('has-changes');
        }
        if (statusText) {
            statusText.textContent = 'Ready';
            statusText.className = 'status-text';
        }

    } catch (error) {
        console.error('Error opening file:', error);
        alert('Error opening file');
    }
}

/**
 * Render code with line numbers in the editor
 */
function renderCode(code) {
    const editor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    const highlightCode = document.getElementById('code-highlight-code');
    const container = document.querySelector('.code-editor-container');

    if (!editor || !lineNumbers) return;

    // Set editor content
    editor.value = code;

    // Set highlighted content
    if (highlightCode) {
        highlightCode.innerHTML = highlightSyntax(code);
    }

    // Generate line numbers
    const lines = code.split('\n');
    lineNumbers.innerHTML = lines.map((_, i) => i + 1).join('<br>');

    // Reset scroll position
    if (container) {
        container.scrollTop = 0;
        container.scrollLeft = 0;
    }
    lineNumbers.scrollTop = 0;

    // Update cursor position display
    updateCursorPosition();
}

/**
 * Simple Python syntax highlighting using placeholder protection
 */
function highlightSyntax(code) {
    // Escape HTML first
    let html = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Placeholder system to protect highlighted content from subsequent regex matches
    // Using a unique marker that won't appear in normal code
    const MARKER = '\uE000';  // Private Use Area character
    const placeholders = [];
    function protect(match, className) {
        const index = placeholders.length;
        placeholders.push(`<span class="${className}">${match}</span>`);
        return `${MARKER}PH${index}PH${MARKER}`;
    }

    // Comments (protect first)
    html = html.replace(/(#.*$)/gm, (m) => protect(m, 'comment'));

    // All strings in one pass (triple-quoted first for priority)
    html = html.replace(/("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g,
        (m) => protect(m, 'string'));

    // Decorators (before keywords to avoid conflicts)
    html = html.replace(/(@\w+)/g, (m) => protect(m, 'decorator'));

    // Keywords
    const keywords = [
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
        'while', 'with', 'yield'
    ];
    const keywordRegex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'g');
    html = html.replace(keywordRegex, (m) => protect(m, 'keyword'));

    // Built-ins
    const builtins = [
        'abs', 'all', 'any', 'bin', 'bool', 'bytes', 'callable', 'chr',
        'dict', 'dir', 'enumerate', 'eval', 'exec', 'filter', 'float',
        'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash',
        'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
        'iter', 'len', 'list', 'locals', 'map', 'max', 'min', 'next',
        'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
        'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
        'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
        'vars', 'zip', 'self'
    ];
    const builtinRegex = new RegExp(`\\b(${builtins.join('|')})\\b`, 'g');
    html = html.replace(builtinRegex, (m) => protect(m, 'builtin'));

    // Numbers
    html = html.replace(/\b(\d+\.?\d*(?:e[+-]?\d+)?)\b/gi, (m) => protect(m, 'number'));

    // Function definitions (match def keyword placeholder followed by function name)
    const phPattern = new RegExp(`${MARKER}PH(\\d+)PH${MARKER}`, 'g');
    html = html.replace(new RegExp(`(${MARKER}PH\\d+PH${MARKER})(\\s+)(\\w+)`, 'g'),
        (match, defPlaceholder, space, funcName) => {
            const idx = parseInt(defPlaceholder.replace(new RegExp(`${MARKER}PH|PH${MARKER}`, 'g'), ''));
            if (placeholders[idx] && placeholders[idx].includes('>def<')) {
                return defPlaceholder + space + protect(funcName, 'function');
            }
            return match;
        });

    // Restore all placeholders
    html = html.replace(new RegExp(`${MARKER}PH(\\d+)PH${MARKER}`, 'g'),
        (_, idx) => placeholders[parseInt(idx)]);

    return html;
}

/**
 * Close the current file
 */
function closeFile() {
    // Check for unsaved changes
    if (hasUnsavedChanges) {
        const confirmDiscard = confirm('You have unsaved changes. Discard them?');
        if (!confirmDiscard) return;
    }

    currentFile = null;
    fileContent = '';
    originalContent = '';
    hasUnsavedChanges = false;

    document.getElementById('file-viewer').style.display = 'none';
    document.getElementById('welcome-view').style.display = 'flex';

    // Remove selection from tree
    document.querySelectorAll('.tree-item.selected').forEach(el => {
        el.classList.remove('selected');
    });
}

/**
 * Run the current file
 */
async function runCurrentFile() {
    if (!currentFile) return;

    const runBtn = document.querySelector('.run-btn');
    runBtn.textContent = '... Running';
    runBtn.disabled = true;

    try {
        const response = await fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ path: currentFile })
        });

        const data = await response.json();

        // Show output viewer
        document.getElementById('file-viewer').style.display = 'none';
        document.getElementById('output-viewer').style.display = 'flex';

        // Update output file name
        const fileName = currentFile.split('/').pop();
        document.getElementById('output-file-name').textContent = `${fileName} (Result)`;

        // Render output
        renderOutput(data);

    } catch (error) {
        console.error('Error running file:', error);
        alert('Error running file');
    } finally {
        runBtn.textContent = '\u25B6 Run';
        runBtn.disabled = false;
    }
}

/**
 * Strip ANSI escape codes from text
 */
function stripAnsi(text) {
    if (!text) return '';
    // Remove all ANSI escape sequences
    return text
        .replace(/\x1b\[[0-9;]*m/g, '')  // Color codes
        .replace(/\x1b\[K/g, '')          // Clear line
        .replace(/\x1b\[\?[0-9]*[a-zA-Z]/g, '')  // Terminal modes
        .replace(/\[38;5;[0-9]+m/g, '')   // 256 color codes (without escape)
        .replace(/\[0m/g, '')             // Reset codes (without escape)
        .replace(/\[[0-9;]*m/g, '');      // Any remaining color codes
}

/**
 * Render test output based on framework type
 * 
 * Framework types (detected by backend via import inspection):
 *   'v2'     - New framework (gravity_field_model.framework)
 *   'v1'     - Legacy framework (GFDTest base class)
 *   'script' - Plain Python script
 */
function renderOutput(data) {
    const container = document.getElementById('output-content');

    if (data.error) {
        container.innerHTML = `
            <div class="output-section">
                <div class="output-section-header">
                    <h3>Error</h3>
                    <span class="status-fail">FAILED</span>
                </div>
                <div class="output-section-content">${escapeHtml(data.error)}</div>
            </div>
        `;
        return;
    }

    // Strip ANSI codes from output
    const cleanOutput = stripAnsi(data.stdout || '');
    const cleanStderr = stripAnsi(data.stderr || '');

    // Route to appropriate renderer based on framework type
    const frameworkType = data.framework || 'script';

    console.log(`Rendering output for framework type: ${frameworkType}`);

    switch (frameworkType) {
        case 'v2':
            // New framework: rich card-based rendering
            container.innerHTML = renderNewFrameworkOutput(cleanOutput);
            break;

        case 'v1':
            // Legacy framework: section-based rendering
            container.innerHTML = renderLegacyFrameworkOutput(cleanOutput);
            break;

        case 'script':
        default:
            // Plain script: simple preformatted output
            container.innerHTML = renderScriptOutput(cleanOutput);
            break;
    }

    // Add stderr if present (same for all framework types)
    if (cleanStderr.trim()) {
        container.innerHTML += `
            <div class="output-section error-section">
                <div class="output-section-header">
                    <h3>Errors</h3>
                    <span class="status-fail">STDERR</span>
                </div>
                <div class="output-section-content">${escapeHtml(cleanStderr)}</div>
            </div>
        `;
    }
}

/**
 * Render plain script output
 */
function renderScriptOutput(output) {
    if (!output.trim()) {
        return '<div class="loading">No output</div>';
    }

    return `
        <div class="output-section">
            <div class="output-section-header">
                <h3>Output</h3>
            </div>
            <div class="output-section-content">
                <pre>${escapeHtml(output)}</pre>
            </div>
        </div>
    `;
}

/**
 * Render legacy (v1) framework output
 */
function renderLegacyFrameworkOutput(output) {
    const sections = parseTestOutput(output);

    if (sections.length === 0) {
        return renderScriptOutput(output);
    }

    let html = '';

    sections.forEach(section => {
        const statusClass = section.status === 'pass' ? 'status-pass' :
            section.status === 'fail' ? 'status-fail' : '';
        const statusText = section.status === 'pass' ? 'PASS' :
            section.status === 'fail' ? 'FAIL' : '';

        const formattedContent = formatSectionContent(section.title, section.content);

        html += `
            <div class="output-section">
                <div class="output-section-header">
                    <h3>${escapeHtml(section.title)}</h3>
                    ${statusText ? `<span class="${statusClass}">${statusText}</span>` : ''}
                </div>
                <div class="output-section-content">${formattedContent}</div>
            </div>
        `;
    });

    return html || renderScriptOutput(output);
}

/**
 * Render new framework output with rich formatting
 */
function renderNewFrameworkOutput(output) {
    const lines = output.split('\n');
    let html = '';
    let currentTest = null;
    let currentSubsection = null;
    let subsectionContent = [];
    let inTable = false;
    let tableLines = [];
    let groupTitle = '';
    let groupSummary = '';
    let summaryLines = [];

    // First pass: extract group title and summary
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Group title is usually followed by dashes
        if (i + 1 < lines.length && /^-{20,}$/.test(lines[i + 1].trim())) {
            if (!groupTitle && !line.includes('[CRITICAL]') && !line.includes('[EXPLORATORY]')) {
                groupTitle = line;
                continue;
            }
        }

        // Summary is at the end (X/Y tests passed)
        if (/^\d+\/\d+\s+tests?\s+passed/i.test(line) || /^\d+\/\d+\s+CRITICAL/i.test(line)) {
            summaryLines.push(line);
        }
    }

    // Create header if we have a group title
    if (groupTitle) {
        html += `
            <div class="framework-header">
                <h2>${escapeHtml(groupTitle)}</h2>
            </div>
        `;
    }

    // Second pass: parse tests
    const tests = parseNewFrameworkTests(lines);

    for (const test of tests) {
        html += renderFrameworkTest(test);
    }

    // Render summary
    if (summaryLines.length > 0) {
        const allPassed = summaryLines.every(l => {
            const match = l.match(/^(\d+)\/(\d+)/);
            return match && match[1] === match[2];
        });

        html += `
            <div class="framework-summary ${allPassed ? 'all-passed' : 'has-failures'}">
                <div class="summary-icon">${allPassed ? '\u2713' : '\u2717'}</div>
                <div class="summary-text">
                    ${summaryLines.map(l => `<div>${escapeHtml(l)}</div>`).join('')}
                </div>
            </div>
        `;
    }

    return html;
}

/**
 * Parse new framework output into test objects
 */
function parseNewFrameworkTests(lines) {
    const tests = [];
    let currentTest = null;
    let currentSubsection = null;
    let subsectionContent = [];
    let inTable = false;
    let tableLines = [];

    const subsectionNames = ['Derivation', 'Model', 'Observations', 'Comparison', 'Commentary'];

    function flushSubsection() {
        if (currentTest && currentSubsection) {
            if (inTable && tableLines.length > 0) {
                currentTest.subsections.push({
                    name: currentSubsection,
                    type: 'table',
                    content: tableLines.slice()
                });
            } else if (subsectionContent.length > 0) {
                currentTest.subsections.push({
                    name: currentSubsection,
                    type: 'text',
                    content: subsectionContent.join('\n')
                });
            }
        }
        currentSubsection = null;
        subsectionContent = [];
        inTable = false;
        tableLines = [];
    }

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        // Skip empty lines and separator lines (but not table borders)
        if (!trimmed) continue;
        if (/^-{20,}$/.test(trimmed)) continue;

        // Check for test header (has [CRITICAL], [STANDARD], or [EXPLORATORY] badge)
        const testHeaderMatch = trimmed.match(/^(.+?)\s*\[(CRITICAL|STANDARD|EXPLORATORY)\]\s*$/);
        if (testHeaderMatch) {
            flushSubsection();
            if (currentTest) tests.push(currentTest);

            currentTest = {
                name: testHeaderMatch[1].trim(),
                level: testHeaderMatch[2],
                question: '',
                status: null,
                subsections: [],
                className: null
            };
            continue;
        }

        // Check for class name (for CLI runner)
        const classMatch = trimmed.match(/^\[class:\s*(\w+)\]$/);
        if (classMatch && currentTest) {
            currentTest.className = classMatch[1];
            continue;
        }

        // Check for test name (ALL CAPS followed by dash separator)
        if (i + 1 < lines.length && /^-{20,}$/.test(lines[i + 1].trim())) {
            const isTestName = trimmed.length > 3 && !trimmed.includes('|') && !trimmed.startsWith('+');
            if (isTestName && !subsectionNames.some(s => trimmed.startsWith(s))) {
                // Skip if this is the group title (first occurrence)
                if (tests.length === 0 && !currentTest) {
                    continue;
                }
                flushSubsection();
                if (currentTest) tests.push(currentTest);

                currentTest = {
                    name: trimmed,
                    level: null,
                    question: '',
                    status: null,
                    subsections: []
                };
                continue;
            }
        }

        // Check for PASS/FAIL status
        if (trimmed === 'PASS') {
            if (currentTest) currentTest.status = 'pass';
            continue;
        }
        if (trimmed === 'FAIL') {
            if (currentTest) currentTest.status = 'fail';
            continue;
        }

        // Check for subsection header
        let isSubsectionHeader = false;
        for (const name of subsectionNames) {
            if (trimmed.startsWith(name)) {
                flushSubsection();
                currentSubsection = trimmed;
                isSubsectionHeader = true;
                break;
            }
        }
        if (isSubsectionHeader) continue;

        // Check for table content (lines with | or starting with +)
        if (trimmed.includes('|') || (trimmed.startsWith('+') && trimmed.includes('-'))) {
            if (!inTable) {
                // Flush any non-table content first
                if (currentSubsection && subsectionContent.length > 0) {
                    currentTest.subsections.push({
                        name: currentSubsection,
                        type: 'text',
                        content: subsectionContent.join('\n')
                    });
                    subsectionContent = [];
                    currentSubsection = 'Table';
                }
                inTable = true;
            }
            tableLines.push(trimmed);
            continue;
        } else if (inTable) {
            // End of table, flush it
            if (currentTest && tableLines.length > 0) {
                currentTest.subsections.push({
                    name: currentSubsection || 'Table',
                    type: 'table',
                    content: tableLines.slice()
                });
            }
            inTable = false;
            tableLines = [];
        }

        // Skip summary lines at the end
        if (/^\d+\/\d+\s+tests?\s+passed/i.test(trimmed) || /^\d+\/\d+\s+CRITICAL/i.test(trimmed)) {
            continue;
        }

        // Question line (after test header, before first subsection)
        if (currentTest && !currentSubsection && trimmed.endsWith('?')) {
            currentTest.question = trimmed;
            continue;
        }

        // Collect subsection content
        if (currentSubsection) {
            subsectionContent.push(trimmed);
        } else if (currentTest && !currentTest.question && trimmed.length > 10) {
            // Might be a question without ? mark
            currentTest.question = trimmed;
        }
    }

    // Flush final content
    flushSubsection();
    if (currentTest) tests.push(currentTest);

    return tests;
}

/**
 * Render a single test from the new framework
 */
function renderFrameworkTest(test) {
    const levelClass = test.level ? test.level.toLowerCase() : 'standard';
    const statusClass = test.status === 'pass' ? 'passed' : test.status === 'fail' ? 'failed' : '';
    const testId = 'test-' + Math.random().toString(36).substr(2, 9);
    // Encode test data as base64 to avoid HTML attribute escaping issues
    const testDataB64 = btoa(unescape(encodeURIComponent(JSON.stringify(test))));

    let html = `
        <div class="framework-test ${statusClass}" id="${testId}" data-test-b64="${testDataB64}">
            <div class="test-header">
                <h3 class="test-name">${escapeHtml(test.name)}</h3>
                <div class="test-actions">
                    <button class="copy-test-btn" onclick="copyTestToClipboard('${testId}')" title="Copy test results to clipboard">
                        <span class="copy-icon">&#128203;</span>
                    </button>
                    <div class="test-badges">
                        ${test.level ? `<span class="level-badge ${levelClass}">${escapeHtml(test.level)}</span>` : ''}
                        ${test.status ? `<span class="status-badge ${statusClass}">${test.status.toUpperCase()}</span>` : ''}
                    </div>
                </div>
            </div>
    `;

    if (test.question) {
        html += `<div class="test-question">${escapeHtml(test.question)}</div>`;
    }

    // Render subsections
    for (const subsection of test.subsections) {
        html += renderFrameworkSubsection(subsection);
    }

    html += '</div>';
    return html;
}

/**
 * Render a subsection from the new framework
 */
function renderFrameworkSubsection(subsection) {
    const name = subsection.name.replace(/\s*\(.*\)$/, ''); // Remove source reference from name
    const sourceMatch = subsection.name.match(/\(([^)]+)\)$/);
    const source = sourceMatch ? sourceMatch[1] : null;

    let html = `
        <div class="test-subsection subsection-${name.toLowerCase().replace(/\s+/g, '-')}">
            <h4 class="subsection-name">
                ${escapeHtml(name)}
                ${source ? `<span class="subsection-source">${escapeHtml(source)}</span>` : ''}
            </h4>
            <div class="subsection-content">
    `;

    if (subsection.type === 'table') {
        html += renderAsciiTable(subsection.content);
    } else {
        html += renderSubsectionText(name, subsection.content);
    }

    html += '</div></div>';
    return html;
}

/**
 * Render ASCII table to HTML
 */
function renderAsciiTable(lines) {
    // Parse ASCII table format like:
    // +--------+------+
    // | Header | Col2 |
    // +--------+------+
    // | data   | val  |
    // +--------+------+

    const dataRows = lines.filter(l => l.includes('|') && !l.match(/^\+[-+]+\+$/));
    if (dataRows.length === 0) return '<pre>' + escapeHtml(lines.join('\n')) + '</pre>';

    let html = '<table class="framework-table">';

    dataRows.forEach((row, idx) => {
        const cells = row.split('|').slice(1, -1).map(c => c.trim());
        if (cells.length === 0) return;

        if (idx === 0) {
            html += '<thead><tr>';
            cells.forEach(cell => {
                html += `<th>${escapeHtml(cell)}</th>`;
            });
            html += '</tr></thead><tbody>';
        } else {
            html += '<tr>';
            cells.forEach(cell => {
                // Highlight OK/FAIL cells
                let cellClass = '';
                if (cell.includes('[OK]') || cell === 'OK') cellClass = 'cell-ok';
                else if (cell.includes('[FAIL]') || cell === 'FAIL') cellClass = 'cell-fail';

                html += `<td class="${cellClass}">${escapeHtml(cell)}</td>`;
            });
            html += '</tr>';
        }
    });

    html += '</tbody></table>';
    return html;
}

/**
 * Render subsection text content
 */
function renderSubsectionText(name, content) {
    const lowerName = name.toLowerCase();

    // Comparison section: render as status list
    if (lowerName === 'comparison') {
        const lines = content.split('\n').filter(l => l.trim());
        let html = '<div class="comparison-list">';

        for (const line of lines) {
            const okMatch = line.match(/\[OK\]\s*(.+?):\s*(.+)/);
            const failMatch = line.match(/\[FAIL\]\s*(.+?):\s*(.+)/);

            if (okMatch) {
                html += `
                    <div class="comparison-item ok">
                        <span class="comparison-icon">\u2713</span>
                        <span class="comparison-metric">${escapeHtml(okMatch[1])}</span>
                        <span class="comparison-value">${escapeHtml(okMatch[2])}</span>
                    </div>
                `;
            } else if (failMatch) {
                html += `
                    <div class="comparison-item fail">
                        <span class="comparison-icon">\u2717</span>
                        <span class="comparison-metric">${escapeHtml(failMatch[1])}</span>
                        <span class="comparison-value">${escapeHtml(failMatch[2])}</span>
                    </div>
                `;
            } else if (line.trim()) {
                html += `<div class="comparison-item">${escapeHtml(line)}</div>`;
            }
        }

        html += '</div>';
        return html;
    }

    // Model/Observations: render as key-value pairs
    if (lowerName === 'model' || lowerName.startsWith('observations')) {
        const lines = content.split('\n').filter(l => l.trim());
        let html = '<div class="metric-list">';

        for (const line of lines) {
            // Match pattern: "Metric Name    1.23e+08" (multiple spaces between)
            const match = line.match(/^(.+?)\s{2,}(\S+.*)$/);
            if (match) {
                html += `
                    <div class="metric-item">
                        <span class="metric-name">${escapeHtml(match[1].trim())}</span>
                        <span class="metric-value">${escapeHtml(match[2].trim())}</span>
                    </div>
                `;
            } else if (line.trim()) {
                html += `<div class="metric-item"><span class="metric-name">${escapeHtml(line)}</span></div>`;
            }
        }

        html += '</div>';
        return html;
    }

    // Derivation: render as steps
    if (lowerName === 'derivation') {
        // Look for EQUATION: and THEREFORE: markers
        let html = '<div class="derivation-steps">';
        const parts = content.split(/\b(EQUATION:|THEREFORE:)\s*/);

        for (let i = 0; i < parts.length; i++) {
            const part = parts[i].trim();
            if (!part) continue;

            if (part === 'EQUATION:') {
                // Next part is the equation
                if (i + 1 < parts.length) {
                    html += `<div class="derivation-equation">${escapeHtml(parts[i + 1].trim())}</div>`;
                    i++;
                }
            } else if (part === 'THEREFORE:') {
                // Next part is the conclusion
                if (i + 1 < parts.length) {
                    html += `<div class="derivation-conclusion">\u2234 ${escapeHtml(parts[i + 1].trim())}</div>`;
                    i++;
                }
            } else {
                // Regular steps
                html += `<div class="derivation-step">${escapeHtml(part)}</div>`;
            }
        }

        html += '</div>';
        return html;
    }

    // Commentary: render as paragraph
    if (lowerName === 'commentary') {
        return `<p class="commentary-text">${escapeHtml(content)}</p>`;
    }

    // Default: preformatted or paragraph
    if (content.includes('\n')) {
        return '<pre>' + escapeHtml(content) + '</pre>';
    }
    return '<p>' + escapeHtml(content) + '</p>';
}

/**
 * Format section content based on section type
 */
function formatSectionContent(title, content) {
    if (!content) return '';

    // Check if this is a tabular section (key-value pairs)
    const tabularSections = ['GFD Model', 'Observations', 'Model', 'Result', 'Comparison', 'Checks'];
    const isTabular = tabularSections.some(s => title.includes(s));

    // Check for JSON table data
    if (content.includes('"headers"') && content.includes('"rows"')) {
        try {
            const jsonMatch = content.match(/\{[^{}]*"headers"[^{}]*"rows"[^{}]*\}/);
            if (jsonMatch) {
                const tableData = JSON.parse(jsonMatch[0]);
                return renderJsonTable(tableData) + escapeHtml(content.replace(jsonMatch[0], ''));
            }
        } catch (e) {
            // Not valid JSON, continue with normal parsing
        }
    }

    if (isTabular) {
        // Parse key-value pairs into a table
        const lines = content.split('\n').filter(l => l.trim());
        const pairs = [];

        for (const line of lines) {
            // Check for key-value pattern (multiple spaces or tabs between key and value)
            const match = line.match(/^(.+?)\s{2,}(.+)$/) || line.match(/^(.+?)\t+(.+)$/);
            if (match) {
                pairs.push({ key: match[1].trim(), value: match[2].trim() });
            } else if (line.trim()) {
                // Not a key-value pair, might be a header or other text
                pairs.push({ key: line.trim(), value: '' });
            }
        }

        if (pairs.length > 0 && pairs.some(p => p.value)) {
            return renderKeyValueTable(pairs);
        }
    }

    // For prose sections like Derivation, join as paragraph
    return '<p>' + escapeHtml(content).replace(/\n\n/g, '</p><p>').replace(/\n/g, ' ') + '</p>';
}

/**
 * Render a key-value table
 */
function renderKeyValueTable(pairs) {
    let html = '<table class="kv-table">';
    for (const pair of pairs) {
        if (pair.value) {
            html += `<tr><td class="kv-key">${escapeHtml(pair.key)}</td><td class="kv-value">${escapeHtml(pair.value)}</td></tr>`;
        } else {
            // Single value row (like a sub-header)
            html += `<tr><td colspan="2" class="kv-header">${escapeHtml(pair.key)}</td></tr>`;
        }
    }
    html += '</table>';
    return html;
}

/**
 * Render a JSON table with headers and rows
 */
function renderJsonTable(data) {
    if (!data.headers || !data.rows) return '';

    let html = '<table class="data-table"><thead><tr>';
    for (const header of data.headers) {
        html += `<th>${escapeHtml(header)}</th>`;
    }
    html += '</tr></thead><tbody>';

    for (const row of data.rows) {
        html += '<tr>';
        for (const cell of row) {
            // Check for status indicators
            let cellClass = '';
            if (cell === 'OK' || cell === 'PASS') cellClass = 'status-pass';
            else if (cell === 'FAIL' || cell === 'ERROR') cellClass = 'status-fail';

            html += `<td class="${cellClass}">${escapeHtml(String(cell))}</td>`;
        }
        html += '</tr>';
    }
    html += '</tbody></table>';
    return html;
}

/**
 * Parse test output into sections
 */
function parseTestOutput(output) {
    const sections = [];
    const lines = output.split('\n');

    let currentSection = null;
    let currentContent = [];
    let globalStatus = null;
    let testName = null;
    let testQuestion = [];

    // Check for PASS/FAIL in output
    if (output.toUpperCase().includes('PASS')) globalStatus = 'pass';
    if (output.toUpperCase().includes('FAIL')) globalStatus = 'fail';

    const sectionKeywords = ['Derivation', 'GFD Model', 'Observations', 'Model', 'Result', 'Comparison', 'Checks', 'Commentary'];

    for (const line of lines) {
        const stripped = line.trim();

        // Skip empty lines and separator lines
        if (!stripped) continue;
        if (/^[=\-_]+$/.test(stripped)) continue;

        // Check if this is an ALL CAPS test name
        if (stripped.length > 5 && stripped === stripped.toUpperCase() && stripped.includes(' ') && !stripped.startsWith('{')) {
            // Save previous section if exists
            if (currentSection && currentContent.length > 0) {
                sections.push({
                    title: currentSection,
                    content: currentContent.join('\n').trim(),
                    status: null
                });
            }

            // Start new test name section
            testName = stripped;
            testQuestion = [];
            currentSection = null;
            currentContent = [];
            continue;
        }

        // Check for section start
        let isSection = false;
        for (const keyword of sectionKeywords) {
            if (stripped.startsWith(keyword)) {
                // If we have a test name and question but haven't added it yet
                if (testName && !sections.some(s => s.title === testName)) {
                    sections.push({
                        title: testName,
                        content: testQuestion.join(' ').trim(),
                        status: globalStatus
                    });
                }

                // Save previous section
                if (currentSection && currentContent.length > 0) {
                    sections.push({
                        title: currentSection,
                        content: currentContent.join('\n').trim(),
                        status: null
                    });
                }
                currentSection = stripped;
                currentContent = [];
                isSection = true;
                break;
            }
        }

        if (isSection) continue;

        // Collect content
        if (currentSection) {
            currentContent.push(stripped);
        } else if (testName) {
            // This is part of the question text
            testQuestion.push(stripped);
        }
    }

    // Add final section
    if (currentSection && currentContent.length > 0) {
        sections.push({
            title: currentSection,
            content: currentContent.join('\n').trim(),
            status: null
        });
    }

    // If no sections found, create one with all content
    if (sections.length === 0 && output.trim()) {
        sections.push({
            title: 'Test Output',
            content: output.trim(),
            status: globalStatus
        });
    }

    // Apply global status to the Checks section or last section
    if (sections.length > 0 && globalStatus) {
        const checksSection = sections.find(s => s.title.includes('Checks'));
        if (checksSection) {
            checksSection.status = globalStatus;
        } else {
            sections[sections.length - 1].status = globalStatus;
        }
    }

    return sections;
}

/**
 * Show source code (go back from output)
 */
function showSource() {
    if (currentFile && fileContent) {
        document.getElementById('output-viewer').style.display = 'none';
        document.getElementById('file-viewer').style.display = 'flex';
    }
}

/**
 * Close output viewer
 */
function closeOutput() {
    document.getElementById('output-viewer').style.display = 'none';
    document.getElementById('welcome-view').style.display = 'flex';
}

/**
 * Run all tests (placeholder)
 */
function runAllTests() {
    alert('Run All Tests: This would execute the full test suite.\nFor now, select individual test files from the file tree.');
}

/**
 * Show statistics
 */
async function showStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        let message = `GDFM Test Statistics\n${'='.repeat(30)}\n\n`;
        message += `Total Tests: ${data.total_tests}\n\n`;
        message += `Categories:\n`;

        data.categories.forEach(cat => {
            message += `  ${cat.name}: ${cat.count} tests\n`;
        });

        alert(message);
    } catch (error) {
        alert('Error loading statistics');
    }
}

/**
 * Show documentation
 */
function showDocs() {
    // Navigate to the reference folder in the tree
    const treeItems = document.querySelectorAll('.tree-item');
    treeItems.forEach(item => {
        if (item.textContent.includes('reference') || item.textContent.includes('docs')) {
            item.classList.add('expanded');
            const children = item.nextElementSibling;
            if (children && children.classList.contains('tree-children')) {
                children.style.display = 'block';
            }
        }
    });

    alert('Documentation files are in the "reference" and "docs" folders.\nExpanded them in the file tree for you.');
}

/**
 * Escape HTML characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Copy test results to clipboard in a formatted text format
 */
function copyTestToClipboard(testId) {
    const testElement = document.getElementById(testId);
    if (!testElement) return;

    const testDataB64 = testElement.getAttribute('data-test-b64');
    if (!testDataB64) return;

    // Decode from base64
    const test = JSON.parse(decodeURIComponent(escape(atob(testDataB64))));
    const formattedText = formatTestForClipboard(test);

    navigator.clipboard.writeText(formattedText).then(() => {
        // Show brief feedback
        const btn = testElement.querySelector('.copy-test-btn');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<span class="copy-icon">&#10003;</span>';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.innerHTML = originalHtml;
            btn.classList.remove('copied');
        }, 1500);
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Format test data as readable text for clipboard
 */
function formatTestForClipboard(test) {
    let lines = [];

    // Header
    lines.push(test.name.toUpperCase());
    if (test.level) lines.push(test.level.toUpperCase());
    if (test.status) lines.push(test.status.toUpperCase());
    lines.push('');

    // Question
    if (test.question) {
        lines.push(test.question);
        lines.push('');
    }

    // Subsections
    for (const subsection of test.subsections) {
        const name = subsection.name.replace(/\s*\(.*\)$/, '');
        const sourceMatch = subsection.name.match(/\(([^)]+)\)$/);
        const source = sourceMatch ? ` (${sourceMatch[1]})` : '';

        lines.push(name + source);

        if (subsection.type === 'table') {
            // Include table as-is
            lines.push(subsection.content.join('\n'));
        } else {
            // Include text content with indentation
            const contentLines = subsection.content.split('\n');
            for (const line of contentLines) {
                if (line.trim()) {
                    lines.push('  ' + line.trim());
                }
            }
        }
        lines.push('');
    }

    // Add CLI command if class name is available
    if (test.className) {
        lines.push('---');
        lines.push('# To run this specific test:');
        lines.push(`python -m gravity_field_model.run_test ${test.className}`);
    }

    return lines.join('\n');
}
