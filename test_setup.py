#!/usr/bin/env python3
"""
Quick Test Script - Test your Pentesting AI setup
"""

import requests

def test_setup():
    print("🔐 Testing Pentesting AI Setup")
    print("=" * 50)
    
    # Test 1: Server health
    try:
        response = requests.get("http://127.0.0.1:8004/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running on port 8004")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not responding: {e}")
        print("   Make sure the server is running!")
        return False
    
    # Test 2: Configuration
    try:
        response = requests.get("http://127.0.0.1:8004/config", timeout=5)
        config = response.json()
        print(f"✅ Configuration loaded")
        print(f"   - Allowlist: {config.get('allowlist', 'Unknown')[:50]}...")
        print(f"   - Model: {config.get('model', 'Unknown')}")
    except Exception as e:
        print(f"❌ Config check failed: {e}")
    
    # Test 3: Quick scan
    print("\n🔍 Running test scan...")
    try:
        scan_data: dict[str, str | bool | list[str]] = {
            "targets": ["http://testphp.vulnweb.com"], 
            "confirm_scope": True
        }
        
        response = requests.post(
            "http://127.0.0.1:8004/scan", 
            json=scan_data, 
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Scan completed successfully")
        else:
            print(f"❌ Scan failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Scan failed: {e}")
        return False
    
    # Test 4: Get results
    print("\n📊 Checking results...")
    try:
        response = requests.get("http://127.0.0.1:8004/report", timeout=5)
        if response.status_code == 200:
            report = response.json()
            summary = report.get('summary', {})
            print("✅ Report generated successfully")
            print(f"   - Assets scanned: {summary.get('assets_scanned', 0)}")
            print(f"   - Total findings: {summary.get('total_findings', 0)}")
            print(f"   - Critical: {summary.get('critical', 0)}")
            print(f"   - High: {summary.get('high', 0)}")
            print(f"   - Medium: {summary.get('medium', 0)}")
            print(f"   - Low: {summary.get('low', 0)}")
            
            # Show first finding
            items = report.get('items', [])
            if items:
                first = items[0]
                print(f"\n🚨 Example finding:")
                print(f"   - Title: {first.get('title', 'Unknown')}")
                print(f"   - Asset: {first.get('asset', 'Unknown')}")
                print(f"   - Priority: {first.get('priority', 'Unknown').upper()}")
                print(f"   - Tags: {', '.join(first.get('tags', []))}")
        else:
            print(f"❌ Report unavailable: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Report check failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Setup test completed!")
    print(f"🌐 Web interface: http://127.0.0.1:8004")
    print(f"📚 Documentation: HOW_TO_USE.md")
    print(f"🎯 Try scanning: http://testphp.vulnweb.com")
    
    return True

if __name__ == "__main__":
    test_setup()
