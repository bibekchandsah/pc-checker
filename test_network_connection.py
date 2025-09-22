#!/usr/bin/env python3
"""
Test script to verify network connection detection logic
"""

import sys
import os
import requests

# Add current directory to path to import update_manager
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from update_manager import UpdateChecker

def test_internet_connection():
    """Test the internet connection detection method"""
    print("Testing internet connection detection...")
    
    # Create a test instance
    checker = UpdateChecker("1.0.0", "test/repo")
    
    # Test the connection method
    connection_available = checker._test_internet_connection()
    
    print(f"Connection available: {connection_available}")
    
    if connection_available:
        print("✅ Internet connection detected successfully")
    else:
        print("❌ No internet connection detected")
    
    return connection_available

def test_github_api_access():
    """Test direct GitHub API access"""
    print("\nTesting GitHub API access...")
    
    try:
        response = requests.get("https://api.github.com", timeout=5)
        print(f"GitHub API status: {response.status_code}")
        if response.status_code == 200:
            print("✅ GitHub API accessible")
        else:
            print(f"⚠️ GitHub API returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ GitHub API connection error")
    except requests.exceptions.Timeout:
        print("❌ GitHub API timeout")
    except Exception as e:
        print(f"❌ GitHub API error: {e}")

def test_individual_endpoints():
    """Test each endpoint individually"""
    print("\nTesting individual endpoints...")
    
    test_urls = [
        "https://www.google.com",
        "https://www.cloudflare.com", 
        "https://httpbin.org/get",
        "https://api.github.com"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"✅ {url} - OK")
            else:
                print(f"⚠️ {url} - Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - Connection Error")
        except requests.exceptions.Timeout:
            print(f"❌ {url} - Timeout")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")

if __name__ == "__main__":
    print("Network Connection Test")
    print("=" * 50)
    
    # Test the connection detection logic
    test_internet_connection()
    
    # Test GitHub API specifically
    test_github_api_access()
    
    # Test individual endpoints
    test_individual_endpoints()
    
    print("\nTest completed!")