# Minimal keyword→tag map
from typing import Dict

MAPS: Dict[str, Dict[str, str]] = {
    "xss": {"cwe": "CWE-79", "owasp": "A03: Injection"},
    "sql injection": {"cwe": "CWE-89", "owasp": "A03: Injection"},
    "ssti": {"cwe": "CWE-94", "owasp": "A03: Injection"},
    "path traversal": {"cwe": "CWE-22", "owasp": "A05: Security Misconfiguration"},
    "csrf": {"cwe": "CWE-352", "owasp": "A08: Software and Data Integrity Failures"},
    "open redirect": {"cwe": "CWE-601", "owasp": "A10: Server-Side Request Forgery"},
    "weak cipher": {"cwe": "CWE-327", "owasp": "A02: Cryptographic Failures"},
    "hardcoded secret": {"cwe": "CWE-798", "owasp": "A02: Cryptographic Failures"},
    "missing authz": {"cwe": "CWE-285", "owasp": "A01: Broken Access Control"},
    "directory listing": {"cwe": "CWE-548", "owasp": "A05: Security Misconfiguration"},
    "outdated component": {"cwe": "CWE-1104", "owasp": "A06: Vulnerable and Outdated Components"},
    "insecure deserialization": {"cwe": "CWE-502", "owasp": "A08: Software and Data Integrity Failures"},
    "xxe": {"cwe": "CWE-611", "owasp": "A05: Security Misconfiguration"},
    "missing https": {"cwe": "CWE-319", "owasp": "A02: Cryptographic Failures"},
    "exposed admin": {"cwe": "CWE-200", "owasp": "A01: Broken Access Control"}
}
