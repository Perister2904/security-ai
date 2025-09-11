import json
from ai.analyst import process_findings_directly

# Load the real normalized findings
with open('data/normalized/zap_real_normalized.json', 'r') as f:
    findings = json.load(f)

print(f'Processing {len(findings)} real vulnerability findings through AI analysis...')

# Generate comprehensive AI security report
analysis = process_findings_directly(findings)

print('\n=== AI SECURITY ANALYSIS OF REAL VULNERABILITIES ===')
print('SUMMARY:')
print(json.dumps(analysis['summary'], indent=2))

print('\nTOP 5 CRITICAL FINDINGS:')
for i, item in enumerate(analysis['items'][:5], 1):
    print(f'{i}. {item["title"]} ({item["priority"]})')
    print(f'   Asset: {item["asset"]}')
    print(f'   Why it matters: {item["why_it_matters"]}')
    print()

# Save the AI analysis
with open('data/ai_real_analysis.json', 'w') as f:
    json.dump(analysis, f, indent=2)

print(f'Complete AI analysis of {len(findings)} findings saved to data/ai_real_analysis.json')
