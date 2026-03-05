#!/usr/bin/env python3
"""
Update system with new API key
"""

import frappe

def update_new_api_key():
    """Update system with new API key: AIzaSyA2IkVNUOx_yG50ifz6T4p0FGwGYndqMe8"""
    
    print("🔧 Updating System with New API Key")
    print("=" * 50)
    
    new_api_key = "AIzaSyA2IkVNUOx_yG50ifz6T4p0FGwGYndqMe8"
    model = "gemini-1.5-flash"
    
    try:
        # Update Assistant CRM Settings
        print("📝 Updating Assistant CRM Settings...")
        settings = frappe.get_single("Assistant CRM Settings")
        settings.api_key = new_api_key
        settings.model_name = model
        settings.ai_provider = "Google Gemini"
        settings.enabled = 1
        settings.response_timeout = 30
        settings.welcome_message = "Hello! I'm WorkCom, your Construction assistant. How can I help you today?"
        settings.save()
        frappe.db.commit()
        
        print(f"✅ Settings updated successfully!")
        print(f"   API Key: ***{new_api_key[-4:]}")
        print(f"   Model: {model}")
        print(f"   Provider: {settings.ai_provider}")
        print(f"   Enabled: {settings.enabled}")
        
        # Update .env.ai file
        print("\n📝 Updating .env.ai file...")
        env_content = f"""# .env.ai (in bench directory)
google_gemini_api_key={new_api_key}
gemini_model={model}"""
        
        with open("/workspace/development/frappe-bench/.env.ai", "w") as f:
            f.write(env_content)
        
        print("✅ .env.ai file updated!")
        
        # Clear caches
        print("\n🧹 Clearing caches...")
        frappe.clear_cache()
        print("✅ Caches cleared!")
        
        # Test the configuration
        print("\n🧪 Testing new configuration...")
        from construction_v1.construction_v1.services.gemini_service import GeminiService
        
        gs = GeminiService()
        print(f"   Gemini Service Model: {gs.model}")
        print(f"   Gemini Service API Key: ***{gs.api_key[-4:] if gs.api_key else 'None'}")
        
        # Test connection
        connection_result = gs.test_connection()
        print(f"   Connection Test: {connection_result}")
        
        if connection_result.get('success'):
            print("✅ New API key is working!")
        else:
            print(f"❌ Connection test failed: {connection_result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating configuration: {str(e)}")
        frappe.db.rollback()
        return False

# Run update if called directly
if __name__ == "__main__":
    update_new_api_key()


