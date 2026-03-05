#!/usr/bin/env python3

import frappe
import json

def comprehensive_diagnostic_analysis():
    """Comprehensive diagnostic analysis of API configuration issues"""
    
    print("🔍 COMPREHENSIVE DIAGNOSTIC ANALYSIS")
    print("=" * 60)
    
    # Step 1: Check if Assistant CRM Settings document exists
    check_settings_document_existence()
    
    # Step 2: Verify database table structure
    verify_database_table_structure()
    
    # Step 3: Check field accessibility
    check_field_accessibility()
    
    # Step 4: Trace execution flow
    trace_execution_flow()
    
    # Step 5: Test get_api_config method directly
    test_get_api_config_method()
    
    # Step 6: Analyze the validation function
    analyze_validation_function()
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC ANALYSIS COMPLETE")

def check_settings_document_existence():
    """Check if Assistant CRM Settings document exists"""
    
    print("\n📋 STEP 1: Checking Assistant CRM Settings Document Existence")
    print("-" * 50)
    
    try:
        # Check if the doctype exists
        doctype_exists = frappe.db.exists("DocType", "Assistant CRM Settings")
        print(f"DocType exists: {'✅ Yes' if doctype_exists else '❌ No'}")
        
        if doctype_exists:
            # Check if the single document exists
            settings_exists = frappe.db.exists("Assistant CRM Settings", "Assistant CRM Settings")
            print(f"Settings document exists: {'✅ Yes' if settings_exists else '❌ No'}")
            
            if settings_exists:
                # Get basic info about the document
                doc_info = frappe.db.get_value("Assistant CRM Settings", "Assistant CRM Settings", 
                                             ["name", "creation", "modified", "enabled"])
                print(f"Document name: {doc_info[0] if doc_info else 'N/A'}")
                print(f"Created: {doc_info[1] if doc_info else 'N/A'}")
                print(f"Modified: {doc_info[2] if doc_info else 'N/A'}")
                print(f"Enabled: {'✅ Yes' if doc_info and doc_info[3] else '❌ No'}")
            else:
                print("❌ Settings document does not exist - this is likely the root cause")
                
        else:
            print("❌ DocType does not exist - major issue")
            
    except Exception as e:
        print(f"❌ Error checking document existence: {str(e)}")

def verify_database_table_structure():
    """Verify the database table structure"""
    
    print("\n🗄️  STEP 2: Verifying Database Table Structure")
    print("-" * 50)
    
    try:
        # Check if table exists
        table_exists = frappe.db.sql("""
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'tabAssistant CRM Settings'
        """, as_dict=True)
        
        if table_exists and table_exists[0]['count'] > 0:
            print("✅ Table 'tabAssistant CRM Settings' exists")
            
            # Get all columns
            columns = frappe.db.sql("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'tabAssistant CRM Settings'
                ORDER BY ORDINAL_POSITION
            """, as_dict=True)
            
            print(f"📊 Table has {len(columns)} columns")
            
            # Check for API configuration fields
            api_fields = [
                'corebusiness_api_url', 'corebusiness_api_key',
                'claims_api_url', 'claims_api_key'
            ]
            
            existing_api_fields = [col['COLUMN_NAME'] for col in columns if col['COLUMN_NAME'] in api_fields]
            missing_api_fields = [field for field in api_fields if field not in existing_api_fields]
            
            print(f"✅ Existing API fields: {existing_api_fields}")
            if missing_api_fields:
                print(f"❌ Missing API fields: {missing_api_fields}")
            else:
                print("✅ All required API fields present")
                
            # Show all columns for reference
            print("\n📋 All table columns:")
            for col in columns:
                print(f"   {col['COLUMN_NAME']}: {col['DATA_TYPE']}")
                
        else:
            print("❌ Table 'tabAssistant CRM Settings' does not exist")
            
    except Exception as e:
        print(f"❌ Error verifying table structure: {str(e)}")

def check_field_accessibility():
    """Check if fields are accessible through Frappe ORM"""
    
    print("\n🔍 STEP 3: Checking Field Accessibility")
    print("-" * 50)
    
    try:
        # Try to get the settings document
        settings = frappe.get_single("Assistant CRM Settings")
        print("✅ Successfully retrieved settings document")
        
        # Check if API fields are accessible
        api_fields = {
            'corebusiness_api_url': 'CoreBusiness API URL',
            'corebusiness_api_key': 'CoreBusiness API Key',
            'claims_api_url': 'Claims API URL',
            'claims_api_key': 'Claims API Key'
        }
        
        for field, label in api_fields.items():
            try:
                value = getattr(settings, field, None)
                if value:
                    # Mask API keys for security
                    display_value = value if 'key' not in field else f"***{value[-4:]}"
                    print(f"✅ {label}: {display_value}")
                else:
                    print(f"⚠️  {label}: Not set (None)")
            except AttributeError:
                print(f"❌ {label}: Field not accessible")
        
        # Check if get_api_config method exists
        if hasattr(settings, 'get_api_config'):
            print("✅ get_api_config method exists")
        else:
            print("❌ get_api_config method not found")
            
    except frappe.DoesNotExistError:
        print("❌ Settings document does not exist")
    except Exception as e:
        print(f"❌ Error checking field accessibility: {str(e)}")

def trace_execution_flow():
    """Trace the execution flow of get_api_config"""
    
    print("\n🔄 STEP 4: Tracing Execution Flow")
    print("-" * 50)
    
    try:
        # Import the function we're testing
        from construction_v1.api.dynamic_data_integration import get_api_config
        
        print("✅ Successfully imported get_api_config function")
        
        # Test CoreBusiness API config
        print("\n🧪 Testing CoreBusiness API config:")
        try:
            cb_config = get_api_config('corebusiness')
            if cb_config:
                print(f"✅ CoreBusiness config retrieved: {cb_config.keys()}")
                print(f"   Base URL: {cb_config.get('base_url', 'Not set')}")
                print(f"   API Key: {'***' + cb_config.get('api_key', '')[-4:] if cb_config.get('api_key') else 'Not set'}")
            else:
                print("❌ CoreBusiness config returned None")
        except Exception as e:
            print(f"❌ Error getting CoreBusiness config: {str(e)}")
        
        # Test Claims API config
        print("\n🧪 Testing Claims API config:")
        try:
            claims_config = get_api_config('claims')
            if claims_config:
                print(f"✅ Claims config retrieved: {claims_config.keys()}")
                print(f"   Base URL: {claims_config.get('base_url', 'Not set')}")
                print(f"   API Key: {'***' + claims_config.get('api_key', '')[-4:] if claims_config.get('api_key') else 'Not set'}")
            else:
                print("❌ Claims config returned None")
        except Exception as e:
            print(f"❌ Error getting Claims config: {str(e)}")
            
    except ImportError as e:
        print(f"❌ Error importing get_api_config: {str(e)}")
    except Exception as e:
        print(f"❌ Error tracing execution flow: {str(e)}")

def test_get_api_config_method():
    """Test the get_api_config method directly on settings object"""
    
    print("\n🎯 STEP 5: Testing get_api_config Method Directly")
    print("-" * 50)
    
    try:
        settings = frappe.get_single("Assistant CRM Settings")
        
        if hasattr(settings, 'get_api_config'):
            print("✅ get_api_config method found on settings object")
            
            # Test CoreBusiness
            try:
                cb_config = settings.get_api_config('corebusiness')
                print(f"CoreBusiness config: {cb_config}")
            except Exception as e:
                print(f"❌ Error calling get_api_config('corebusiness'): {str(e)}")
            
            # Test Claims
            try:
                claims_config = settings.get_api_config('claims')
                print(f"Claims config: {claims_config}")
            except Exception as e:
                print(f"❌ Error calling get_api_config('claims'): {str(e)}")
                
        else:
            print("❌ get_api_config method not found on settings object")
            print("Available methods:", [method for method in dir(settings) if not method.startswith('_')])
            
    except Exception as e:
        print(f"❌ Error testing get_api_config method: {str(e)}")

def analyze_validation_function():
    """Analyze the validation function that's failing"""
    
    print("\n🔬 STEP 6: Analyzing Validation Function")
    print("-" * 50)
    
    try:
        from construction_v1.api.api_testing_framework import validate_api_configuration
        
        print("✅ Successfully imported validate_api_configuration")
        
        # Run the validation and capture detailed output
        result = validate_api_configuration()
        
        print("📊 Validation result:")
        print(json.dumps(result, indent=2))
        
        # Analyze each component
        if 'corebusiness_api' in result:
            cb_result = result['corebusiness_api']
            print(f"\nCoreBusinessAPI analysis:")
            print(f"   Status: {cb_result.get('status')}")
            print(f"   Error: {cb_result.get('error')}")
            
        if 'claims_api' in result:
            claims_result = result['claims_api']
            print(f"\nClaims API analysis:")
            print(f"   Status: {claims_result.get('status')}")
            print(f"   Error: {claims_result.get('error')}")
            
    except ImportError as e:
        print(f"❌ Error importing validation function: {str(e)}")
    except Exception as e:
        print(f"❌ Error analyzing validation function: {str(e)}")

if __name__ == "__main__":
    frappe.init(site="dev")
    frappe.connect()
    comprehensive_diagnostic_analysis()

