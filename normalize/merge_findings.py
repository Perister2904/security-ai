from typing import List, Dict, Any

def merge_findings(list_of_lists: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    for findings_list in list_of_lists:
        findings.extend(findings_list)
    return findings
