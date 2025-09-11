from typing import List, Dict, Any
from enrich.maps import MAPS

def enrich_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []
    for f in findings:
        tags: List[str] = []
        title = str(f.get('title', '')).lower()
        description = str(f.get('description', '')).lower()
        
        for keyword, mapping in MAPS.items():
            if keyword in title or keyword in description:
                f['cwe'] = mapping['cwe']
                f['owasp'] = mapping['owasp'] 
                tags = [mapping['cwe'], mapping['owasp']]
                break
                
        f['tags'] = tags
        enriched.append(f)
    return enriched
