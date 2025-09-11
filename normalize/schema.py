# Unified Finding Schema
from typing import Union, List, Dict, Any

SCHEMA: Dict[str, Any] = {
    "tool": str,
    "asset": str,
    "title": str,
    "severity": str,
    "description": str,
    "evidence": str,
    "cve": Union[str, None],
    "cwe": Union[str, None],
    "owasp": Union[str, None],
    "references": List[str],
    "raw_links": List[str]
}
