#!/usr/bin/env python3
"""
Quick test script to verify the API works locally
"""
import requests
import json
import time
import subprocess
import signal
import os
import sys

def test_api():
    # Test data from the assignment
    test_payload = {
        "age": 0.02,
        "sex": -0.044,
        "bmi": 0.06,
        "bp": -0.03,
        "s1": -0.02,
        "s2": 0.03,
        "s3": -0.02,
        "s4": 0.02,
        "s5": 0.02,
        "s6": -0.001
    }
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        print("Testing /health endpoint...")
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test predict endpoint
        print("\nTesting /predict endpoint...")
        response = requests.post(
            f"{base_url}/predict",
            json=test_payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        print("\n✅ API tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure it's running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing Diabetes Clinic Triage API")
    print("Make sure to start the API first with: cd src && python api.py")
    print("Then run this test script in another terminal")
    
    test_api()