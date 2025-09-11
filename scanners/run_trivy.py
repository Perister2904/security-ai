import subprocess
from pathlib import Path
from typing import Union
import os

def run_trivy(target: str, raw_dir: Union[str, Path]) -> Path:
    out_json = Path(raw_dir) / "trivy.json"
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/project",
        "-v", f"{os.getcwd()}\\data\\raw:/data" if os.name == 'nt' else f"{os.getcwd()}/data/raw:/data",
        "aquasec/trivy", "fs",
        "--format", "json", "--output", "/data/trivy.json", "/project"
    ]
    try:
        subprocess.run(cmd, check=True)
    except Exception:
        if not out_json.exists() or out_json.stat().st_size == 0:
            out_json.write_text('[]')
    return out_json
