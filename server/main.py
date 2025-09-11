import os
import json
import sys
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from subprocess import Popen
from typing import Optional, Dict, Any
import threading
import time

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
UI_DIR = Path(__file__).parent / "ui"
MODEL = os.getenv("MODEL", "llama3.1:8b")
DEFAULT_TARGET = os.getenv("DEFAULT_TARGET", "http://testphp.vulnweb.com")
LOG_PATH = DATA_DIR / "scan.log"
REPORT_PATH = DATA_DIR / "ai_report.json"

# Scan process globals
scan_process: Optional[Popen[bytes]] = None
scan_target: Optional[str] = None
scan_started_at: float = 0.0
scan_lock = threading.Lock()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/ui", StaticFiles(directory=UI_DIR, html=True), name="ui")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config")
def config():
    return {"model": MODEL, "default_target": DEFAULT_TARGET}

def _is_running() -> bool:
    global scan_process
    return scan_process is not None and scan_process.poll() is None

def _start_scan(target: str) -> None:
    global scan_process, scan_target, scan_started_at
    with scan_lock:
        if _is_running():
            raise RuntimeError("Scan already in progress")
        
        # Clean up old results to ensure fresh scan
        if REPORT_PATH.exists():
            REPORT_PATH.unlink()
        if LOG_PATH.exists():
            LOG_PATH.unlink()
        
        # Clean up old raw data files
        raw_files = ["zap.json", "nuclei.json", "trivy.json", "nuclei.jsonl"]
        for filename in raw_files:
            raw_file = RAW_DIR / filename
            if raw_file.exists():
                raw_file.unlink()
        
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        
        # Open log file for writing (truncate previous) with UTF-8 encoding
        log_f = open(LOG_PATH, "w", encoding="utf-8", errors="replace")
        cmd = [sys.executable, "scripts/scan_all.py", "--targets", target, "--confirm-scope"]
        
        # Set environment for UTF-8 support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        scan_process = Popen(cmd, stdout=log_f, stderr=log_f, cwd=PROJECT_ROOT, env=env)
        scan_target = target
        scan_started_at = time.time()

@app.post("/scan")
async def scan(request: Request) -> Dict[str, Any]:
    body = await request.json()
    targets = body.get("targets", [])
    confirm_scope = body.get("confirm_scope", False)
    if not targets:
        raise HTTPException(status_code=400, detail="No targets provided")
    target = targets[0]
    if not confirm_scope:
        raise HTTPException(status_code=400, detail="Scope confirmation required.")
    try:
        _start_scan(target)
        return {"status": "started", "target": target}
    except RuntimeError:
        return {"status": "running", "target": scan_target}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {e}")

@app.get("/status")
async def status() -> Dict[str, Any]:
    running = _is_running()
    started = scan_started_at if running and scan_started_at > 0 else None
    duration = (time.time() - scan_started_at) if running and scan_started_at > 0 else None
    report_exists = REPORT_PATH.exists()
    log_exists = LOG_PATH.exists()
    exit_code = None
    if not running and scan_process is not None:
        exit_code = scan_process.poll()
    return {
        "running": running,
        "target": scan_target,
        "started_at": started,
        "duration_sec": round(duration, 1) if duration else None,
        "report_ready": report_exists and not running,  # Only ready when scan is complete
        "log_size": LOG_PATH.stat().st_size if log_exists else 0,
        "exit_code": exit_code,
        "timestamp": time.time()  # Add timestamp for cache busting
    }

@app.get("/log")
async def log(lines: int = 200):  # type: ignore
    if not LOG_PATH.exists():
        return PlainTextResponse("No log yet", status_code=200)
    try:
        with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
            content = f.readlines()
        tail = content[-lines:] if lines > 0 else content
        return PlainTextResponse("".join(tail))
    except Exception as e:
        return PlainTextResponse(f"Log read error: {e}", status_code=500)

@app.get("/report")
def report():  # type: ignore
    if not REPORT_PATH.exists():
        return JSONResponse({"error": "No report found."}, status_code=404)
    
    try:
        # Read the report with fresh data
        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        # Add metadata about when this report was generated
        report_data["_meta"] = {
            "generated_at": REPORT_PATH.stat().st_mtime,
            "target": scan_target,
            "fresh_scan": True
        }
        
        return JSONResponse(report_data, status_code=200)
    except Exception as e:
        return JSONResponse({"error": f"Failed to read report: {str(e)}"}, status_code=500)

@app.get("/")
def index():
    return HTMLResponse((UI_DIR / "index.html").read_text())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004)
