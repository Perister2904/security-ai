import json
from typing import List, Dict, Any, Union
from pathlib import Path

def normalize_zap(zap_json_path: Union[str, Path]) -> List[Dict[str, Any]]:
    try:
        with open(zap_json_path, 'r') as f:
            data = json.load(f)
        # Handle both array and object formats
        if isinstance(data, list):
            return []  # Empty array, no alerts
        elif isinstance(data, dict):
            sites = data.get('site', [])  # type: ignore
            if not sites:
                return []
            alerts = sites[0].get('alerts', []) if sites else []  # type: ignore
        else:
            return []
    except Exception:
        return []
    
    findings: List[Dict[str, Any]] = []
    for item in alerts:  # type: ignore
        finding: Dict[str, Any] = {
            "tool": "zap",
            "asset": str(item.get('url', '')),  # type: ignore
            "title": str(item.get('name', '')),  # type: ignore
            "severity": str(item.get('risk', 'info')).lower(),  # type: ignore
            "description": str(item.get('desc', '')),  # type: ignore
            "evidence": str(item.get('evidence', '')),  # type: ignore
            "cve": None,
            "cwe": item.get('cweid', None),  # type: ignore
            "owasp": None,
            "references": str(item.get('reference', '')).split() if item.get('reference') else [],  # type: ignore
            "raw_links": [f"file://{zap_json_path}"]
        }
        findings.append(finding)
    return findings
