import json
from typing import List, Dict, Any, Union
from pathlib import Path

def normalize_trivy(trivy_json_path: Union[str, Path]) -> List[Dict[str, Any]]:
    try:
        with open(trivy_json_path, 'r') as f:
            data = json.load(f)
        # Handle both array and object formats
        if isinstance(data, list):
            return []  # Empty array, no vulnerabilities
        elif not isinstance(data, dict):
            return []
    except Exception:
        return []
    
    findings: List[Dict[str, Any]] = []
    results = data.get('Results', [])  # type: ignore
    for result in results:  # type: ignore
        vulnerabilities = result.get('Vulnerabilities', [])  # type: ignore
        for vuln in vulnerabilities:  # type: ignore
            cwe_ids = vuln.get('CweIDs', [])  # type: ignore
            finding: Dict[str, Any] = {
                "tool": "trivy",
                "asset": str(result.get('Target', '')),  # type: ignore
                "title": str(vuln.get('Title', '')),  # type: ignore
                "severity": str(vuln.get('Severity', 'info')).lower(),  # type: ignore
                "description": str(vuln.get('Description', '')),  # type: ignore
                "evidence": str(vuln.get('PrimaryURL', '')),  # type: ignore
                "cve": vuln.get('VulnerabilityID', None),  # type: ignore
                "cwe": cwe_ids[0] if cwe_ids else None,  # type: ignore
                "owasp": None,
                "references": vuln.get('References', []) or [],  # type: ignore
                "raw_links": [f"file://{trivy_json_path}"]
            }
            findings.append(finding)
    return findings
