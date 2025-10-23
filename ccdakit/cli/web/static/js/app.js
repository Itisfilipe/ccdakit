// Format a validation issue with enhanced display and collapsible sections
function formatValidationIssue(issue, index, severity) {
    // Check if we have parsed data for enhanced display
    if (issue.parsed) {
        const parsed = issue.parsed;
        const issueId = `issue-${severity}-${index}`;

        let html = '<div class="validation-issue">';

        // Issue summary (always visible)
        html += '<div class="issue-summary">';
        html += `<span class="issue-icon">${severity === 'error' ? '❌' : '⚠️'}</span>`;
        html += '<div class="issue-content">';

        // Location
        if (parsed.simplified_path) {
            html += `<div class="issue-location"><strong>Location:</strong> <code>${escapeHtml(parsed.simplified_path)}</code></div>`;
        }

        // Requirement
        html += `<div class="issue-requirement">${escapeHtml(parsed.requirement)}</div>`;

        // Template info if available
        if (parsed.template_id || parsed.template_name) {
            html += '<div class="issue-template">';
            if (parsed.template_name) {
                html += `<span class="template-name">${escapeHtml(parsed.template_name)}</span>`;
            }
            if (parsed.template_id) {
                html += ` <span class="template-id">(${escapeHtml(parsed.template_id)})</span>`;
            }
            if (parsed.conf_number) {
                html += ` <span class="conf-number">CONF:${escapeHtml(parsed.conf_number)}</span>`;
            }
            html += '</div>';
        }

        html += '</div>'; // .issue-content
        html += '</div>'; // .issue-summary

        // Suggestions (collapsible)
        if (parsed.suggestions && parsed.suggestions.length > 0) {
            html += '<details class="issue-details">';
            html += '<summary>💡 How to Fix</summary>';
            html += '<ul class="issue-suggestions">';
            parsed.suggestions.forEach(suggestion => {
                html += `<li>${escapeHtml(suggestion)}</li>`;
            });
            html += '</ul>';
            html += '</details>';
        }

        // Technical details (collapsible)
        html += '<details class="issue-details">';
        html += '<summary>🔍 Technical Details</summary>';
        html += '<div class="issue-technical">';

        if (parsed.full_xpath) {
            html += `<div><strong>Full XPath:</strong><br><code class="xpath-code">${escapeHtml(parsed.full_xpath)}</code></div>`;
        }

        html += `<div><strong>Original Message:</strong><br>${escapeHtml(parsed.original_message)}</div>`;

        html += '</div>'; // .issue-technical
        html += '</details>';

        html += '</div>'; // .validation-issue

        return html;
    } else {
        // Fallback for non-parsed errors (e.g., XSD validation)
        const message = typeof issue === 'string' ? issue : (issue.message || issue.raw_message || 'Unknown error');
        return `<div class="validation-issue simple"><div class="issue-summary">${escapeHtml(message)}</div></div>`;
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Warning banner functionality - persist dismissal for the browser session
function dismissBanner() {
    const banner = document.getElementById('warningBanner');
    banner.style.display = 'none';
    // Remember dismissal for the browser session
    sessionStorage.setItem('disclaimerDismissed', 'true');
}

// Show banner only if not dismissed in this session
document.addEventListener('DOMContentLoaded', function() {
    const banner = document.getElementById('warningBanner');
    if (banner) {
        // Check if user dismissed the banner in this session
        const isDismissed = sessionStorage.getItem('disclaimerDismissed');
        if (!isDismissed) {
            banner.style.display = 'block';
        }
    }
});

// Tab switching functionality
function switchTab(event, tabType, index = '') {
    event.preventDefault();

    // Get the parent form element
    const form = event.target.closest('form') || event.target.closest('.feature-container');

    // Handle compare page with multiple tab sets
    const suffix = index ? `-${index}` : '';

    // Update tab buttons
    const tabButtons = form.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => {
        if (btn.closest('.input-tabs') === event.target.closest('.input-tabs')) {
            btn.classList.remove('active');
        }
    });
    event.target.classList.add('active');

    // Update tab content
    const fileInput = form.querySelector(`#file-input${suffix}`);
    const pasteInput = form.querySelector(`#paste-input${suffix}`);

    if (fileInput && pasteInput) {
        if (tabType === 'file') {
            fileInput.classList.add('active');
            pasteInput.classList.remove('active');
        } else {
            fileInput.classList.remove('active');
            pasteInput.classList.add('active');
        }
    }
}

async function validateDocument(event) {
    event.preventDefault();
    const form = event.target;
    const resultDiv = document.getElementById('validateResult');
    const formData = new FormData(form);

    // Check which input method is active
    const fileInput = form.querySelector('#file-input');
    const pasteInput = form.querySelector('#paste-input');

    if (pasteInput.classList.contains('active')) {
        // Remove file from FormData if using paste
        formData.delete('file');
    } else {
        // Remove content from FormData if using file
        formData.delete('content');
    }

    resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Validating... This may take a minute for large files.</p></div>';

    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<div class="result-box error-box"><h3>Error</h3><p>${data.error}</p></div>`;
            return;
        }

        let html = '';
        let hasResults = false;

        for (const [validator, result] of Object.entries(data)) {
            hasResults = true;
            const statusClass = result.is_valid ? 'success-box' : 'error-box';
            html += `<div class="result-box ${statusClass}">`;
            html += `<h3>${validator.toUpperCase()} Validation</h3>`;
            html += `<p><strong>Status:</strong> ${result.is_valid ? '✅ PASSED' : '❌ FAILED'}</p>`;
            html += `<p><strong>Errors:</strong> ${result.error_count} | <strong>Warnings:</strong> ${result.warning_count}</p>`;

            if (result.errors && result.errors.length > 0) {
                html += '<h4>Errors:</h4>';
                html += '<div class="validation-issues">';
                result.errors.slice(0, 20).forEach((error, index) => {
                    html += formatValidationIssue(error, index, 'error');
                });
                if (result.errors.length > 20) {
                    html += `<div class="issue-summary"><em>... and ${result.errors.length - 20} more errors</em></div>`;
                }
                html += '</div>';
            }

            if (result.warnings && result.warnings.length > 0) {
                html += '<h4>Warnings:</h4>';
                html += '<div class="validation-issues">';
                result.warnings.slice(0, 10).forEach((warning, index) => {
                    html += formatValidationIssue(warning, index, 'warning');
                });
                if (result.warnings.length > 10) {
                    html += `<div class="issue-summary"><em>... and ${result.warnings.length - 10} more warnings</em></div>`;
                }
                html += '</div>';
            }
            html += '</div>';
        }

        if (!hasResults) {
            html = '<div class="result-box error-box"><h3>No Results</h3><p>No validation results were returned.</p></div>';
        }

        resultDiv.innerHTML = html;
    } catch (error) {
        console.error('Validation error:', error);
        resultDiv.innerHTML = `<div class="result-box error-box"><h3>Error</h3><p>${error.message}</p></div>`;
    }
}

async function generateDocument(event) {
    event.preventDefault();
    const form = event.target;
    const resultDiv = document.getElementById('generateResult');

    const documentType = form.document_type.value;
    const sections = Array.from(form.querySelectorAll('input[name="sections"]:checked')).map(cb => cb.value);

    resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Generating...</p></div>';

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ document_type: documentType, sections: sections })
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<div class="result-box error-box">Error: ${data.error}</div>`;
        } else {
            const blob = new Blob([data.xml], { type: 'application/xml' });
            const url = URL.createObjectURL(blob);
            resultDiv.innerHTML = `
                <div class="result-box success-box">
                    <h3>✅ Document Generated!</h3>
                    <p><a href="${url}" download="${documentType}.xml">Download XML File</a></p>
                    <details>
                        <summary>Preview XML</summary>
                        <pre>${data.xml.substring(0, 1000)}...</pre>
                    </details>
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="result-box error-box">Error: ${error.message}</div>`;
    }
}

async function convertDocument(event) {
    event.preventDefault();
    const form = event.target;
    const resultDiv = document.getElementById('convertResult');
    const formData = new FormData(form);

    // Check which input method is active
    const pasteInput = form.querySelector('#paste-input');

    if (pasteInput && pasteInput.classList.contains('active')) {
        // Remove file from FormData if using paste
        formData.delete('file');
    } else {
        // Remove content from FormData if using file
        formData.delete('content');
    }

    resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Converting...</p></div>';

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<div class="result-box error-box">Error: ${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `
                <div class="result-box success-box">
                    <h3>✅ Converted Successfully!</h3>
                    <div class="result-html">${data.html}</div>
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="result-box error-box">Error: ${error.message}</div>`;
    }
}

async function compareDocuments(event) {
    event.preventDefault();
    const form = event.target;
    const resultDiv = document.getElementById('compareResult');
    const formData = new FormData(form);

    // Check which input methods are active
    const pasteInput1 = form.querySelector('#paste-input-1');
    const pasteInput2 = form.querySelector('#paste-input-2');

    if (pasteInput1 && pasteInput1.classList.contains('active')) {
        formData.delete('file1');
    } else {
        formData.delete('content1');
    }

    if (pasteInput2 && pasteInput2.classList.contains('active')) {
        formData.delete('file2');
    } else {
        formData.delete('content2');
    }

    resultDiv.innerHTML = '<div class="loading"><div class="spinner"></div><p>Comparing...</p></div>';

    try {
        const response = await fetch('/api/compare', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<div class="result-box error-box">Error: ${data.error}</div>`;
        } else {
            const comp = data.comparison;
            let html = '<div class="result-box success-box">';
            html += `<h3>Comparison: ${data.file1_name} vs ${data.file2_name}</h3>`;

            if (comp.patient_differences.length > 0) {
                html += '<h4>Patient Differences:</h4><ul>';
                comp.patient_differences.forEach(diff => {
                    html += `<li><strong>${diff.field}:</strong> ${diff.file1} → ${diff.file2}</li>`;
                });
                html += '</ul>';
            }

            if (comp.sections_only_in_1.length > 0) {
                html += `<h4>Sections only in ${data.file1_name}:</h4><ul>`;
                comp.sections_only_in_1.forEach(s => html += `<li>${s}</li>`);
                html += '</ul>';
            }

            if (comp.sections_only_in_2.length > 0) {
                html += `<h4>Sections only in ${data.file2_name}:</h4><ul>`;
                comp.sections_only_in_2.forEach(s => html += `<li>${s}</li>`);
                html += '</ul>';
            }

            if (comp.section_differences.length > 0) {
                html += '<h4>Section Entry Count Differences:</h4><ul>';
                comp.section_differences.forEach(diff => {
                    html += `<li><strong>${diff.section}:</strong> ${diff.file1_entries} → ${diff.file2_entries} entries</li>`;
                });
                html += '</ul>';
            }

            if (comp.patient_differences.length === 0 && comp.sections_only_in_1.length === 0 &&
                comp.sections_only_in_2.length === 0 && comp.section_differences.length === 0) {
                html += '<p>✅ Documents are structurally identical!</p>';
            }

            html += '</div>';
            resultDiv.innerHTML = html;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="result-box error-box">Error: ${error.message}</div>`;
    }
}
