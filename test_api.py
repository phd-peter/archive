#!/usr/bin/env python3
import requests
import json
import time

def test_health_check():
    """서버 상태 확인"""
    print("=== Health Check ===")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_process_image():
    """이미지 처리 API 테스트"""
    print("\n=== Image Processing Test ===")
    
    # 테스트용 이미지 URL (Google Drive 공개 링크)
    test_data = {
        "web_content_link": "https://drive.google.com/uc?id=1ScHjp5j8fHpMxnOvTBLH8H6kpAybb2SI&export=download",
        "labels": ["invoice_number", "date", "total_amount"]
    }
    
    try:
        print(f"Testing with data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            "http://localhost:8000/process",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Results:")
            for item in result["results"]:
                print(f"  {item['label']}: {item['text']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"API test failed: {e}")

def test_with_custom_labels():
    """사용자 정의 라벨 테스트"""
    print("\n=== Custom Labels Test ===")
    
    test_data = {
        "web_content_link": "https://drive.google.com/uc?id=1ScHjp5j8fHpMxnOvTBLH8H6kpAybb2SI&export=download",
        "labels": ["company_name", "address", "phone_number"]
    }
    
    try:
        print(f"Testing with custom labels: {test_data['labels']}")
        
        response = requests.post(
            "http://localhost:8000/process",
            json=test_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Results:")
            for item in result["results"]:
                print(f"  {item['label']}: {item['text']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Custom labels test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting API Tests...")
    print("Make sure the server is running on http://localhost:8000")
    
    # 서버가 시작될 때까지 잠시 대기
    time.sleep(2)
    
    # 테스트 실행
    if test_health_check():
        test_process_image()
        test_with_custom_labels()
    else:
        print("❌ Server is not running. Please start the server first with: python main.py")
    
    print("\n✅ Tests completed!") 