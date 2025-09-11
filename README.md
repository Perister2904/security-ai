# 🛡️ Security AI - Automated Penetration Testing Dashboard

> **Disclaimer:** This tool is for authorized security testing only. Run ONLY with written authorization on systems you own or have explicit permission to test.

An AI-powered security scanning platform that combines multiple Docker-based security tools with intelligent analysis and a modern web interface.

## 🎯 Features

- **Multi-Scanner Integration**: Combines OWASP ZAP, Nuclei, and Trivy for comprehensive security assessment
- **Real-time Web Dashboard**: Monitor scans in real-time with live log streaming
- **AI-Powered Analysis**: Local LLM analysis via Ollama for vulnerability assessment
- **Docker-Based**: Isolated, consistent scanning environment using Docker containers
- **Fresh Results**: Cache-busting mechanisms ensure accurate, up-to-date scan results
- **Local-Only**: No cloud dependencies, all processing happens locally
- **No Database Required**: File-based storage for simplicity

## 🏗️ Architecture

```
security-ai/
├── server/          # FastAPI web server and UI
│   ├── main.py      # Main server application  
│   └── ui/          # Modern web interface
├── scanners/        # Docker-based security scanners
│   ├── run_zap.py   # OWASP ZAP integration
│   ├── run_nuclei.py # Nuclei vulnerability scanner
│   └── run_trivy.py # Trivy security scanner
├── normalize/       # Data normalization modules
├── enrich/          # Vulnerability enrichment with CWE/OWASP
├── ai/              # Local AI analysis engine
└── scripts/         # Main scanning orchestration
```

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) - For running security scanners
- [Python 3.10+](https://www.python.org/downloads/) - Main application runtime
- [Ollama](https://ollama.com/download) - Local LLM for AI analysis

### 1. Clone & Install
```bash
# Clone the repository
git clone https://github.com/yourusername/security-ai.git
cd security-ai

# Set up Python environment
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac  
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment
Edit `.env` file with your settings:
```env
MODEL=llama3.1:8b
DEFAULT_TARGET=http://testphp.vulnweb.com
SCAN_TIMEOUT=300
LOG_LEVEL=INFO
```

### 3. Set Up Local LLM
```bash
# Pull the AI model for analysis
ollama pull llama3.1:8b
```

### 4. Start the Application
```bash
# Start the web server
python server/main.py
```

### 5. Access the Dashboard
Open your browser to `http://127.0.0.1:8004`

## 🔧 Usage

### Web Interface
1. Navigate to `http://127.0.0.1:8004`
2. Enter target URL (e.g., `http://testphp.vulnweb.com`)
3. Click "Run Scan" to start security assessment
4. Monitor real-time progress in Live Log
5. Review comprehensive results when complete

### Command Line
```bash
python scripts/scan_all.py --targets http://example.com --confirm-scope
```

## 📊 Security Scanners

| Scanner | Purpose | Container Image |
|---------|---------|-----------------|
| **OWASP ZAP** | Web application security testing | `ghcr.io/zaproxy/zaproxy:stable` |
| **Nuclei** | Fast vulnerability scanner | `projectdiscovery/nuclei:latest` |
| **Trivy** | Container and dependency scanning | `aquasec/trivy:latest` |

## 🛠️ Key Features

### Real-time Scanning
- ✅ Live status updates during execution
- ✅ Real-time log streaming
- ✅ Progress indicators for each scanner
- ✅ Fresh results with cache-busting

### AI-Powered Analysis
- 🤖 Local LLM vulnerability assessment
- 📊 Risk prioritization and scoring
- 💡 Actionable remediation recommendations
- 🏷️ CWE/OWASP classification

### Modern Web Interface
- 📱 Responsive design
- ⚡ Real-time updates
- 🎨 Professional security dashboard
- 🔍 Detailed vulnerability reports

## 🚨 Security Notice

⚠️ **IMPORTANT**: This tool is designed for authorized security testing only.

- ✅ Only scan systems you own or have explicit permission to test
- ⚠️ Be aware of rate limiting and potential service disruption
- 🔍 Review scan targets carefully before execution
- 🔒 Store scan results securely
- 📋 Ensure compliance with applicable laws and regulations

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OWASP ZAP](https://www.zaproxy.org/) - Leading web application security testing tool
- [Nuclei](https://nuclei.projectdiscovery.io/) - Fast and customizable vulnerability scanner
- [Trivy](https://trivy.dev/) - Comprehensive security scanner for containers
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Ollama](https://ollama.com/) - Run large language models locally

## 📞 Support

Need help? Here's how to get support:

1. 📖 Check the documentation above
2. 🐛 Search [existing issues](https://github.com/yourusername/security-ai/issues)
3. 🆕 Create a [new issue](https://github.com/yourusername/security-ai/issues/new) with:
   - Detailed problem description
   - Steps to reproduce
   - System information
   - Log files (if applicable)

---

**Built with ❤️ for the security community**
python scripts/scan_all.py --targets http://localhost:3000 --confirm-scope
```

### 5. Start Server & UI
```sh
uvicorn server.main:app --reload
# Visit http://localhost:8000
```

## Docker Compose (Optional)
See `docker-compose.yml` for scanner containers. Scanners run on-demand via Python subprocess.

## Troubleshooting
- If Docker/LLM not available, pipeline will mock minimal JSON for demo.
- All data stored under `./data`.

## License
MIT
