import os
import sys
import json
import argparse
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8:replace'

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanners.run_zap import run_zap
from scanners.run_nuclei import run_nuclei
from scanners.run_trivy import run_trivy
from normalize.normalize_zap import normalize_zap
from normalize.normalize_nuclei import normalize_nuclei
from normalize.normalize_trivy import normalize_trivy
from normalize.merge_findings import merge_findings
from enrich.enrich import enrich_findings
from ai.analyst import run_analyst

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

os.makedirs(RAW_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--targets', nargs='+', required=True)
    parser.add_argument('--confirm-scope', action='store_true')
    args = parser.parse_args()

    print(f"[TARGET] Starting security scan for: {args.targets}")
        
    if not args.confirm_scope:
        print("Scope confirmation required.", file=sys.stderr)
        sys.exit(1)

    findings = []
    # Run scanners
    zap_out = run_zap(args.targets[0], RAW_DIR)
    nuclei_out = run_nuclei(args.targets[0], RAW_DIR)
    trivy_out = run_trivy(args.targets[0], RAW_DIR)
    # Normalize
    zap_findings = normalize_zap(zap_out)
    nuclei_findings = normalize_nuclei(nuclei_out)
    trivy_findings = normalize_trivy(trivy_out)
    findings = merge_findings([zap_findings, nuclei_findings, trivy_findings])
    (DATA_DIR / "findings.raw.json").write_text(json.dumps(findings, indent=2))
    # Enrich
    enriched = enrich_findings(findings)
    (DATA_DIR / "findings.enriched.json").write_text(json.dumps(enriched, indent=2))
    # AI analyst
    ai_report = run_analyst(enriched)
    (DATA_DIR / "ai_report.json").write_text(json.dumps(ai_report, indent=2))
    print(f"Scan complete. Report: {DATA_DIR / 'ai_report.json'}")

if __name__ == "__main__":
    main()
