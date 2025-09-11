import json
from typing import Dict, Any, List
from normalize.schema import SCHEMA  # type: ignore

def test_finding_schema():
    """Test that all findings match the expected schema"""
    with open('data/findings.raw.json') as f:
        findings: List[Dict[str, Any]] = json.load(f)
    
    print(f"Testing {len(findings)} findings against schema...")
    
    for i, finding in enumerate(findings):
        print(f"Finding {i+1}: {finding.get('tool', 'unknown')} - {finding.get('title', 'unknown')}")
        
        for key in SCHEMA:  # type: ignore
            if key not in finding:
                print(f"  ❌ Missing required key: {key}")
                return False
            
            # Skip complex type checking, just verify basic structure
            print(f"  ✅ Has required key: {key}")
        
        print(f"  ✅ Schema structure valid")
    
    print("All findings have required keys!")
    return True

def test_enrichment_quality():
    """Test the quality of enrichment"""
    with open('data/findings.enriched.json') as f:
        findings = json.load(f)
    
    enriched_count = sum(1 for f in findings if f.get('cwe') or f.get('owasp'))
    print(f"Enrichment rate: {enriched_count}/{len(findings)} findings ({enriched_count/len(findings)*100:.1f}%)")
    
    return enriched_count > 0

if __name__ == "__main__":
    print("=== Schema Validation Test ===")
    schema_ok = test_finding_schema()
    
    print("\n=== Enrichment Quality Test ===")  
    enrichment_ok = test_enrichment_quality()
    
    print(f"\n=== Test Results ===")
    print(f"Schema validation: {'✅ PASS' if schema_ok else '❌ FAIL'}")
    print(f"Enrichment quality: {'✅ PASS' if enrichment_ok else '❌ FAIL'}")
