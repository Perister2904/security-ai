import os
import json
from typing import Dict, Any, List
import requests
from pathlib import Path

def process_findings_directly(enriched_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process findings directly when AI is unavailable"""
    if not enriched_findings:
        return {
            "summary": {"assets_scanned": 0, "total_findings": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "items": []
        }
    
    # Count severity levels
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    assets: set[str] = set()
    
    items: List[Dict[str, Any]] = []
    for finding in enriched_findings:
        # Extract asset from finding
        asset = finding.get('asset', 'Unknown')
        assets.add(asset)
        
        # Map severity
        severity = finding.get('severity', 'info').lower()
        if severity in severity_counts:
            severity_counts[severity] += 1
        else:
            severity_counts['info'] += 1
            
        # Create report item
        item: Dict[str, Any] = {
            "asset": asset,
            "priority": severity,
            "title": finding.get('title', 'Security Finding'),
            "tags": [
                f"CWE-{finding.get('cwe', 'Unknown')}" if finding.get('cwe') else "Security Issue",
                finding.get('owasp', 'Security Risk')
            ],
            "why_it_matters": finding.get('description', 'Security vulnerability detected')[:200] + "...",
            "fix_steps": [
                "Review the security finding details",
                "Apply appropriate security controls",
                "Test the fix thoroughly",
                "Monitor for similar issues"
            ],
            "source_tools": [finding.get('tool', 'scanner')],
            "evidence": finding.get('raw_links', ['file://data/raw/scan_results.json'])
        }
        items.append(item)
    
    return {
        "summary": {
            "assets_scanned": len(assets),
            "total_findings": len(enriched_findings),
            **severity_counts
        },
        "items": items
    }

def run_analyst(enriched_findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    system_prompt_path = Path(__file__).parent / "prompts" / "system.txt"
    user_template_path = Path(__file__).parent / "prompts" / "user_template.txt"
    
    system = system_prompt_path.read_text()
    user_template = user_template_path.read_text()
    user = user_template + "\nFindings:\n" + json.dumps(enriched_findings)
    
    model = os.getenv("MODEL", "llama3.1:8b")
    url = "http://localhost:11434/api/generate"
    payload: Dict[str, Any] = {
        "model": model,
        "system": system,
        "prompt": user,
        "stream": False
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        # Ollama returns {response: ...}
        out = resp.json().get('response', '{}')
        return json.loads(out)  # type: ignore
    except Exception as e:
        print(f"AI analyst unavailable ({e}), using direct findings processing")
        # Process real findings directly when AI is unavailable
        return process_findings_directly(enriched_findings)
