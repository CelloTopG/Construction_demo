#!/usr/bin/env python3
"""
Comprehensive test of new API key
"""

import frappe
import requests
import json

def comprehensive_api_test():
    """Comprehensive test of the new API key configuration"""
    
    print("🔧 Comprehensive API Key Test")
    print("=" * 60)
    
    new_api_key = "AIzaSyA2IkVNUOx_yG50ifz6T4p0FGwGYndqMe8"
    
    # Test 1: Direct API Call
    print("\n1️⃣ Direct Google Gemini API Test")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={new_api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Hello! Please respond with a simple greeting."
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 100,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                ai_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"   ✅ Direct API Success: {ai_response}")
            else:
                print(f"   ❌ No candidates: {response_data}")
        else:
            print(f"   ❌ Direct API Failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Direct API Error: {str(e)}")
    
    # Test 2: Check Current Settings
    print("\n2️⃣ Current Settings Check")
    try:
        settings = frappe.get_single("Assistant CRM Settings")
        print(f"   API Key: ***{settings.api_key[-4:] if settings.api_key else 'None'}")
        print(f"   Model: {settings.model_name}")
        print(f"   Provider: {settings.ai_provider}")
        print(f"   Enabled: {settings.enabled}")
        
        # Update with new key if different
        if settings.api_key != new_api_key:
            print("   🔧 Updating settings with new API key...")
            settings.api_key = new_api_key
            settings.model_name = "gemini-1.5-flash"
            settings.ai_provider = "Google Gemini"
            settings.enabled = 1
            settings.save()
            frappe.db.commit()
            print("   ✅ Settings updated!")
        else:
            print("   ✅ Settings already have new API key")
            
    except Exception as e:
        print(f"   ❌ Settings Error: {str(e)}")
    
    # Test 3: Gemini Service Test
    print("\n3️⃣ Gemini Service Test")
    try:
        from construction_v1.construction_v1.services.gemini_service import GeminiService
        gs = GeminiService()
        
        print(f"   Service API Key: ***{gs.api_key[-4:] if gs.api_key else 'None'}")
        print(f"   Service Model: {gs.model}")
        
        # Test connection
        connection_result = gs.test_connection()
        print(f"   Connection Test: {connection_result}")
        
        # Test message processing
        print("   Testing message processing...")
        ai_response = gs.process_message(
            message="Hello, this is a test",
            user_context={"user": "Administrator"},
            chat_history=[]
        )
        
        print(f"   Process Message Result: {ai_response}")
        
        if isinstance(ai_response, dict) and ai_response.get("response"):
            print(f"   ✅ Gemini Service Working: {ai_response['response'][:100]}...")
        else:
            print(f"   ❌ Gemini Service Issue: {ai_response}")
            
    except Exception as e:
        print(f"   ❌ Gemini Service Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Complete Chat API Test
    print("\n4️⃣ Complete Chat API Test")
    try:
        from construction_v1.api.chat import send_message
        
        result = send_message(
            message="Hello WorkCom, this is a test with the new API key",
            session_id="comprehensive_test_456"
        )
        
        print(f"   Chat API Result: {result}")
        
        if isinstance(result, dict):
            if result.get("success") and result.get("response"):
                print(f"   ✅ Chat API Working: {result['response'][:100]}...")
            else:
                print(f"   ❌ Chat API Issue: {result}")
        else:
            print(f"   ❌ Unexpected result type: {type(result)}")
            
    except Exception as e:
        print(f"   ❌ Chat API Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("🎯 Comprehensive Test Complete")

# Run test if called directly
if __name__ == "__main__":
    comprehensive_api_test()


