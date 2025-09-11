#!/usr/bin/env python3
"""Test script to run normalization pipeline without Docker scanners"""
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from normalize.normalize_zap import normalize_zap  
from normalize.normalize_nuclei import normalize_nuclei
from normalize.normalize_trivy import normalize_trivy
from normalize.merge_findings import merge_findings
from enrich.enrich import enrich_findings
from ai.analyst import run_analyst

DATA_DIR = Path(__file__).parent / "data"

def main():
    print("Processing mock data...")
    
    # Run normalizers
    zap_findings = normalize_zap(DATA_DIR / "raw" / "zap.json")
    nuclei_findings = normalize_nuclei(DATA_DIR / "raw" / "nuclei.jsonl") 
    trivy_findings = normalize_trivy(DATA_DIR / "raw" / "trivy.json")
    
    # Merge findings
    findings = merge_findings([zap_findings, nuclei_findings, trivy_findings])
    (DATA_DIR / "findings.raw.json").write_text(json.dumps(findings, indent=2))
    print(f"Raw findings: {len(findings)} items")
    
    # Enrich
    enriched = enrich_findings(findings)
    (DATA_DIR / "findings.enriched.json").write_text(json.dumps(enriched, indent=2))
    print(f"Enriched findings: {len(enriched)} items")
    
    # AI analyst
    ai_report = run_analyst(enriched)
    (DATA_DIR / "ai_report.json").write_text(json.dumps(ai_report, indent=2))
    print(f"AI report generated with {ai_report.get('summary', {}).get('total_findings', 0)} findings")
    print(f"Report saved to: {DATA_DIR / 'ai_report.json'}")

if __name__ == "__main__":
    main()
