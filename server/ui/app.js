// Global state for intervals
let pollInterval = null;
let logInterval = null;
let currentScanTarget = null;
let lastReportTime = 0;

// Load configuration from server
async function loadConfig() {
  try {
    const res = await fetch('/config?t=' + Date.now());
    if (res.ok) {
      const cfg = await res.json();
      const targetInput = document.getElementById('target');
      if (targetInput && !targetInput.value) {
        targetInput.value = cfg.default_target || 'http://testphp.vulnweb.com';
      }
    }
  } catch (e) {
    console.warn('Config load failed', e);
  }
}

// Update status display
function setStatus(html) {
  const statusEl = document.getElementById('status');
  if (statusEl) statusEl.innerHTML = html;
}

// Update scan button state
function setButton(running) {
  const btn = document.getElementById('scan-btn');
  if (!btn) return;
  if (running) {
    btn.disabled = true;
    btn.textContent = 'Scanning...';
  } else {
    btn.disabled = false;
    btn.textContent = 'Run Scan';
  }
}

// Fetch scan status from server
async function fetchStatus() {
  try {
    const res = await fetch('/status?t=' + Date.now());
    if (!res.ok) return;
    const s = await res.json();
    
    // Only process if we have an active scan target
    if (!currentScanTarget) {
      console.log('No active scan target, ignoring status update');
      return;
    }
    
    const parts = [];
    parts.push(`<b>Running:</b> ${s.running ? '🟢 Yes' : '🔴 No'}`);
    if (s.target) parts.push(`<b>Target:</b> ${s.target}`);
    if (s.started_at) parts.push(`<b>Started:</b> ${new Date(s.started_at * 1000).toLocaleTimeString()}`);
    if (s.duration_sec) parts.push(`<b>Duration:</b> ${s.duration_sec}s`);
    if (s.exit_code !== null && s.exit_code !== undefined) parts.push(`<b>Exit Code:</b> ${s.exit_code}`);
    parts.push(`<b>Report Ready:</b> ${s.report_ready ? '✅ Yes' : '⏳ No'}`);
    parts.push(`<b>Log Size:</b> ${s.log_size} bytes`);
    
    setStatus(parts.join(' | '));
    setButton(s.running);
    
    // If scan just completed and we have a fresh report
    if (s.report_ready && !s.running && s.target === currentScanTarget) {
      console.log('Scan completed, fetching fresh report...');
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait a moment for file to flush
      fetchReport();
      
      // Stop polling when done
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
      }
      if (logInterval) {
        clearInterval(logInterval);
        logInterval = null;
      }
      // Keep target to show final results
    }
  } catch (e) {
    console.warn('Status error', e);
  }
}

// Fetch scan logs from server
async function fetchLog() {
  try {
    const res = await fetch('/log?lines=500&t=' + Date.now());
    if (!res.ok) return;
    const text = await res.text();
    const pre = document.getElementById('log');
    if (pre) {
      pre.textContent = text;
      pre.scrollTop = pre.scrollHeight;
    }
  } catch (e) {
    // Ignore log fetch errors silently
  }
}

// Fetch vulnerability report from server
async function fetchReport() {
  try {
    const res = await fetch('/report?t=' + Date.now());
    if (!res.ok) {
      document.getElementById('report').innerHTML = '<p>No report found yet.</p>';
      document.getElementById('summary').innerHTML = '';
      return;
    }
    const data = await res.json();
    
    // Check if this is a fresh report
    const reportTime = data._meta?.generated_at || 0;
    if (reportTime <= lastReportTime) {
      console.log('Skipping old/cached report');
      return;
    }
    lastReportTime = reportTime;
    
    console.log('Rendering fresh report with', data.items?.length || 0, 'findings');
    renderReport(data);
  } catch (error) {
    console.error('Report fetch error:', error);
    document.getElementById('report').innerHTML = '<p>❌ Error loading report.</p>';
  }
}

// Render vulnerability report in UI
function renderReport(data) {
  const summary = data.summary || {};
  let summaryHtml = `<h2>🛡️ Security Scan Summary</h2><ul>`;
  for (const k in summary) {
    summaryHtml += `<li><b>${k.replace(/_/g, ' ')}:</b> ${summary[k]}</li>`;
  }
  summaryHtml += `</ul>`;
  
  if (data._meta?.target) {
    summaryHtml += `<p><b>Scanned Target:</b> ${data._meta.target}</p>`;
  }
  if (data._meta?.generated_at) {
    summaryHtml += `<p><b>Report Generated:</b> ${new Date(data._meta.generated_at * 1000).toLocaleString()}</p>`;
  }
  
  document.getElementById('summary').innerHTML = summaryHtml;

  const items = data.items || [];
  if (!items.length) {
    document.getElementById('report').innerHTML = '<p>✅ No security vulnerabilities detected in this fresh scan.</p>';
    return;
  }
  
  const cards = items.map(item => `
    <div class="card">
      <div class="priority ${item.priority || 'info'}">${(item.priority || 'info').toUpperCase()}</div>
      <h3>${item.asset || 'Target Asset'}</h3>
      <h4>${item.title || 'Security Finding'}</h4>
      <div><b>Tags:</b> ${(item.tags || []).join(', ')}</div>
      <div><b>Why it matters:</b> ${(item.why_it_matters || '').substring(0, 300)}${item.why_it_matters && item.why_it_matters.length > 300 ? '...' : ''}</div>
      <div><b>Fix steps:</b><ul>${(item.fix_steps || []).map(s => `<li>${s}</li>`).join('')}</ul></div>
      <div><b>Source tools:</b> ${(item.source_tools || []).join(', ')}</div>
    </div>
  `).join('');
  
  document.getElementById('report').innerHTML = `<h2>🔍 Fresh Security Findings (${items.length})</h2>` + cards;
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Set up form submission handler
  const form = document.getElementById('scan-form');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const target = document.getElementById('target').value.trim();
      if (!target) {
        alert('Please enter a target URL');
        return;
      }
      
      // Clear old results immediately
      currentScanTarget = target;
      lastReportTime = 0;
      document.getElementById('summary').innerHTML = '';
      document.getElementById('report').innerHTML = '<p>🚀 Starting fresh vulnerability scan with Docker containers...</p>';
      const logEl = document.getElementById('log');
      if (logEl) logEl.textContent = 'Initializing new scan...';

      try {
        const res = await fetch('/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ targets: [target], confirm_scope: true })
        });
        
        if (!res.ok) {
          const text = await res.text();
          alert('Scan failed to start: ' + text);
          setButton(false);
          currentScanTarget = null;
          return;
        }
        
        const result = await res.json();
        console.log('Fresh scan started for:', target, result);
        
        // Clear any existing intervals
        if (pollInterval) clearInterval(pollInterval);
        if (logInterval) clearInterval(logInterval);
        
        // Start polling for status and logs with faster intervals
        pollInterval = setInterval(fetchStatus, 2000);  // Faster polling
        logInterval = setInterval(fetchLog, 1500);      // Faster log updates
        
        // Initial fetch
        fetchStatus();
        fetchLog();
        
      } catch (err) {
        console.error('Network error:', err);
        alert('Network error: ' + err.message);
        setButton(false);
      }
    });
  }

  // Load initial state
  loadConfig();
  fetchStatus();
  fetchLog();
});
