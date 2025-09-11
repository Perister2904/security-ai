# 🔐 Pentesting AI - Complete Usage Guide

## **🚀 Quick Start (5 Minutes)**

### **1. Your server is running at: http://127.0.0.1:8004**
Open your browser and go there. You'll see the dashboard like in the screenshot.

### **2. Scan something right now:**
In the text box, enter one of these targets and click "Run Scan":

- `http://testphp.vulnweb.com` (legal vulnerable website)
- `http://localhost:3000` (if you have a local web server)
- `http://127.0.0.1` (your own computer)

### **3. Wait 30-60 seconds, refresh the page to see results**

---

## **📊 What The Scan Results Mean**

### **Summary Section:**
- **assets_scanned**: How many websites/IPs were tested
- **total_findings**: Number of security issues found
- **critical/high/medium/low**: Severity levels (critical = fix immediately)

### **Individual Findings:**
Each finding shows you:
- **Asset**: The specific URL/IP that has the issue
- **Title**: What the vulnerability is called
- **Tags**: Technical categories (CWE-79 = XSS, CWE-89 = SQL injection)
- **Why it matters**: Business risk explanation
- **Fix steps**: Actual things you can do to fix it
- **Evidence**: Links to raw scanner output files

---

## **🎯 What To Scan (Safe & Legal)**

### **✅ Legal Practice Websites (Always OK to scan):**
```
http://testphp.vulnweb.com
http://demo.testfire.net  
http://zero.webappsecurity.com
https://portswigger.net/web-security/
```

### **✅ Your Own Systems:**
```
http://localhost:3000
http://127.0.0.1:8080
https://your-own-website.com
```

### **❌ Never Scan These Without Permission:**
- Government websites (.gov)
- Banking/financial sites
- Any website you don't own
- Social media platforms
- Cloud services (AWS, Google, etc.)

---

## **🔧 Advanced Configuration**

### **Current Status:**
- ✅ Allowlist: **DISABLED** (you can scan anything)
- ✅ Server: Running on port 8004
- ✅ Mock data: Working (Docker not required)
- ✅ AI analysis: Using local mock responses

### **Enable Real Docker Scanning:**
1. Install [Docker Desktop](https://docker.com/products/docker-desktop)
2. Restart your computer
3. Run a scan - it will automatically use real OWASP ZAP, Nuclei, and Trivy

### **Enable AI Analysis:**
1. Install [Ollama](https://ollama.com/download)
2. Run: `ollama pull llama3.1:8b`
3. Run a scan - it will use real AI to analyze findings

---

## **🛠️ Practical Examples**

### **Example 1: Test a Vulnerable Website**
```powershell
# In PowerShell:
Invoke-RestMethod -Uri "http://127.0.0.1:8004/scan" -Method Post -ContentType "application/json" -Body '{"targets": ["http://testphp.vulnweb.com"], "confirm_scope": true}'
```

### **Example 2: Test Your Localhost**
```powershell
# Scan your own computer:
Invoke-RestMethod -Uri "http://127.0.0.1:8004/scan" -Method Post -ContentType "application/json" -Body '{"targets": ["http://127.0.0.1"], "confirm_scope": true}'
```

### **Example 3: Multiple Targets**
```powershell
# Scan multiple sites at once:
Invoke-RestMethod -Uri "http://127.0.0.1:8004/scan" -Method Post -ContentType "application/json" -Body '{"targets": ["http://testphp.vulnweb.com", "http://demo.testfire.net"], "confirm_scope": true}'
```

---

## **📋 Common Issues & Solutions**

### **"Target not in allowlist"**
- **Solution**: Allowlist is disabled on port 8004, use that server

### **"Scope confirmation required"**
- **Solution**: Always add `"confirm_scope": true` to your scan requests

### **Scan takes forever**
- **Solution**: Without Docker, it uses mock data (instant). With Docker, real scans take 2-5 minutes

### **No results showing**
- **Solution**: Refresh the browser page, or check `http://127.0.0.1:8004/report`

### **Want to scan your own website**
- **Solution**: You can! Just make sure you actually own it or have permission

---

## **🔍 Understanding Vulnerabilities Found**

### **Common Findings & What They Mean:**

**SQL Injection (CWE-89)**
- **What it is**: Attacker can access your database
- **Risk**: Steal all your data, delete everything
- **Fix**: Use parameterized queries, input validation

**Cross-Site Scripting/XSS (CWE-79)**  
- **What it is**: Attacker can run JavaScript in victim's browser
- **Risk**: Steal login cookies, redirect users, deface site
- **Fix**: HTML encode all output, Content Security Policy

**Directory Listing (CWE-200)**
- **What it is**: Web server shows file/folder contents
- **Risk**: Exposes sensitive files, source code
- **Fix**: Configure web server to disable directory browsing

**Insecure SSL/TLS (CWE-319)**
- **What it is**: Weak encryption or expired certificates  
- **Risk**: Data can be intercepted, man-in-the-middle attacks
- **Fix**: Update SSL certificates, disable old TLS versions

---

## **⚡ Power User Tips**

### **1. Batch Scanning**
Create a file `targets.txt`:
```
http://testphp.vulnweb.com
http://demo.testfire.net
http://127.0.0.1:8080
```

### **2. Automated Scanning**
```powershell
# Scan every hour:
while ($true) {
    Invoke-RestMethod -Uri "http://127.0.0.1:8004/scan" -Method Post -ContentType "application/json" -Body '{"targets": ["http://your-site.com"], "confirm_scope": true}'
    Start-Sleep 3600
}
```

### **3. Export Results**
```powershell
# Save results to file:
Invoke-RestMethod -Uri "http://127.0.0.1:8004/report" | ConvertTo-Json | Out-File "scan-results-$(Get-Date -Format 'yyyy-MM-dd').json"
```

### **4. Monitor Specific Issues**
```powershell
# Check for critical findings:
$report = Invoke-RestMethod -Uri "http://127.0.0.1:8004/report"
if ($report.summary.critical -gt 0) {
    Write-Host "CRITICAL ISSUES FOUND!" -ForegroundColor Red
}
```

---

## **🎓 Learning Path**

### **Beginner (Week 1):**
1. Scan `http://testphp.vulnweb.com` 
2. Read each finding carefully
3. Research the CWE numbers on [cwe.mitre.org](https://cwe.mitre.org)

### **Intermediate (Week 2-4):**
1. Set up local vulnerable apps (DVWA, WebGoat)
2. Install Docker for real scanning
3. Scan your own projects

### **Advanced (Month 2+):**
1. Install Ollama for AI analysis
2. Write custom nuclei templates
3. Integrate with CI/CD pipelines
4. Set up continuous monitoring

---

## **⚖️ Legal & Ethical Guidelines**

### **✅ Always Legal:**
- Your own websites/applications
- Intentionally vulnerable practice sites
- Local development environments
- Systems you have written permission to test

### **⚠️ Get Permission First:**
- Company websites (even if you work there)
- Client systems
- Shared hosting environments
- Cloud instances

### **❌ Never Legal:**
- Random websites on the internet
- Government systems
- Banking/financial sites
- Other people's property without permission

### **� Documentation:**
- Keep logs of what you scan and when
- Save permission emails/documents
- Document findings and remediation
- Follow responsible disclosure for real vulnerabilities

**Remember**: Being able to do something doesn't mean you should. Always ask "Do I have permission?" before scanning.
