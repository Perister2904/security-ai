import json
from typing import List, Dict, Any, Union, cast
from pathlib import Path

def normalize_nuclei(nuclei_json_path: Union[str, Path]) -> List[Dict[str, Any]]:
    try:
        with open(nuclei_json_path, 'r') as f:
            content = f.read().strip()
        if not content:
            return []
        
        # Try parsing as JSON array first, then fall back to JSONL
        try:
            data_raw = json.loads(content)
            if isinstance(data_raw, list):
                # It's a JSON array
                data = cast(List[Any], data_raw)
            else:
                # It's a single JSON object, wrap in array
                data = [data_raw]
        except json.JSONDecodeError:
            # Try parsing as JSONL (one JSON per line)
            data = [json.loads(line) for line in content.split('\n') if line.strip()]
    except Exception:
        return []
    
    findings: List[Dict[str, Any]] = []
    for item in data:
        if isinstance(item, dict):
            finding: Dict[str, Any] = {
                "tool": "nuclei",
                "asset": str(item.get('host', '')),  # type: ignore
                "title": str(item.get('template', '')),  # type: ignore
                "severity": str(item.get('severity', 'info')).lower(),  # type: ignore
                "description": str(item.get('description', '')),  # type: ignore
                "evidence": str(item.get('matched-at', '')),  # type: ignore
                "cve": item.get('cve', None),  # type: ignore
                "cwe": item.get('cwe', None),  # type: ignore
                "owasp": None,
                "references": item.get('references', []) or [],  # type: ignore
                "raw_links": [f"file://{nuclei_json_path}"]
            }
            findings.append(finding)
    return findings
