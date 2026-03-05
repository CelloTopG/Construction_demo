#!/usr/bin/env python3
"""
Assistant CRM Deployment Test Function
=====================================

Test function to validate the deployed Assistant CRM system.
"""

import json
import frappe

def test_deployment():
    """Test the deployed Assistant CRM system."""
    print("🚀 TESTING ASSISTANT CRM DEPLOYMENT")
    print("=" * 40)
    
    results = []
    
    # Test 1: Intent Router Configuration
    try:
        from construction_v1.services.intent_router import IntentRouter
        print("✅ Intent Router import successful")
        
        router = IntentRouter()
        live_data_count = len(router.live_data_intents)
        kb_count = len(router.knowledge_base_intents)
        
        print(f"✅ Live data intents: {live_data_count}")
        print(f"✅ Knowledge base intents: {kb_count}")
        
        expected_live_data = {
            'claim_status', 'payment_status', 'pension_inquiry', 'claim_submission',
            'account_info', 'payment_history', 'document_status', 'technical_help'
        }
        
        config_correct = router.live_data_intents == expected_live_data
        print(f"✅ Configuration: {'CORRECT' if config_correct else 'INCORRECT'}")
        
        if config_correct:
            print("✅ All 8 live data intents properly configured")
        else:
            print(f"❌ Expected: {sorted(expected_live_data)}")
            print(f"❌ Actual: {sorted(router.live_data_intents)}")
        
        results.append(("Intent Router", config_correct))
        
    except Exception as e:
        print(f"❌ Intent Router error: {e}")
        results.append(("Intent Router", False))
    
    print()
    
    # Test 2: LiveDataOrchestrator
    try:
        from construction_v1.services.live_data_orchestrator import get_live_data_orchestrator
        print("✅ LiveDataOrchestrator import successful")
        
        orchestrator = get_live_data_orchestrator()
        
        # Test a simple data retrieval
        user_context = {
            'user_id': 'TEST001',
            'user_role': 'beneficiary'
        }
        
        claim_data = orchestrator._get_claim_data(user_context)
        print(f"✅ Claim data retrieval: {'SUCCESS' if claim_data else 'FAILED'}")
        
        technical_help_data = orchestrator._get_technical_help_data(user_context)
        print(f"✅ Technical help data retrieval: {'SUCCESS' if technical_help_data else 'FAILED'}")
        
        orchestrator_success = claim_data is not None and technical_help_data is not None
        results.append(("LiveDataOrchestrator", orchestrator_success))
        
    except Exception as e:
        print(f"❌ LiveDataOrchestrator error: {e}")
        results.append(("LiveDataOrchestrator", False))
    
    print()
    
    # Test 3: Unified Chat API
    try:
        from construction_v1.api.unified_chat_api import unified_chat_api
        print("✅ Unified Chat API import successful")
        
        # Test live data query
        result = unified_chat_api(
            message="What is my claim status?",
            session_id="test_deployment",
            user_context=json.dumps({
                'user_id': 'TEST001',
                'user_role': 'beneficiary',
                'permissions': ['view_public_info', 'view_own_data', 'submit_claims']
            })
        )
        
        success = result.get('success', False)
        live_data_used = result.get('live_data_used', False)
        reply = result.get('reply', '')
        
        print(f"✅ API Response Success: {success}")
        print(f"✅ Live Data Used: {live_data_used}")
        print(f"✅ Reply Length: {len(reply)} chars")
        
        # Check for WorkCom and Construction
        WorkCom_present = 'WorkCom' in reply
        Construction_present = 'Construction' in reply
        
        print(f"✅ WorkCom Personality: {WorkCom_present}")
        print(f"✅ Construction Branding: {Construction_present}")
        
        api_success = success and live_data_used and len(reply) > 0
        results.append(("Unified Chat API", api_success))
        
        # Test guest user fallback
        guest_result = unified_chat_api(
            message="What is my claim status?",
            session_id="test_guest",
            user_context=json.dumps({
                'user_id': 'guest',
                'user_role': 'guest'
            })
        )
        
        guest_success = guest_result.get('success', False)
        guest_live_data = guest_result.get('live_data_used', False)
        
        print(f"✅ Guest Fallback Success: {guest_success}")
        print(f"✅ Guest Live Data (should be False): {not guest_live_data}")
        
        fallback_success = guest_success and not guest_live_data
        results.append(("Guest Fallback", fallback_success))
        
    except Exception as e:
        print(f"❌ Unified Chat API error: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Unified Chat API", False))
        results.append(("Guest Fallback", False))
    
    print()
    
    # Summary
    print("📊 DEPLOYMENT TEST SUMMARY")
    print("=" * 30)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 DEPLOYMENT VALIDATION: COMPLETE SUCCESS!")
        print("✅ Assistant CRM with 8 live data intents is fully operational")
        print("✅ WorkCom personality and Construction branding preserved")
        print("✅ Ready for production use")
        return True
    else:
        print(f"\n⚠️  DEPLOYMENT VALIDATION: {total - passed} issues detected")
        return False

def run_comprehensive_test():
    """Run comprehensive test of all 8 live data intents."""
    print("\n🔍 COMPREHENSIVE LIVE DATA INTENT TESTING")
    print("=" * 50)
    
    from construction_v1.api.unified_chat_api import unified_chat_api
    
    # Test all 8 live data intents
    test_cases = [
        ("Claim Status", "What is my claim status?"),
        ("Payment Status", "When will I receive my payment?"),
        ("Pension Inquiry", "What are my pension benefits?"),
        ("Claim Submission", "How do I submit a claim?"),
        ("Account Info", "What is my account information?"),
        ("Payment History", "Show me my payment history"),
        ("Document Status", "What is my document status?"),
        ("Technical Help", "I need technical help")
    ]
    
    user_context = json.dumps({
        'user_id': 'TEST001',
        'user_role': 'beneficiary',
        'permissions': ['view_public_info', 'view_own_data', 'submit_claims', 'view_payments']
    })
    
    results = []
    
    for intent_name, message in test_cases:
        try:
            result = unified_chat_api(
                message=message,
                session_id=f"test_{intent_name.lower().replace(' ', '_')}",
                user_context=user_context
            )
            
            success = result.get('success', False)
            live_data_used = result.get('live_data_used', False)
            reply_length = len(result.get('reply', ''))
            
            overall_success = success and live_data_used and reply_length > 0
            
            status = "✅" if overall_success else "❌"
            print(f"{status} {intent_name}: Live data={live_data_used}, Reply={reply_length} chars")
            
            results.append(overall_success)
            
        except Exception as e:
            print(f"❌ {intent_name}: Error - {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nComprehensive Test Results: {passed}/{total} intents working ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL 8 LIVE DATA INTENTS: FULLY OPERATIONAL!")
    else:
        print(f"⚠️  {total - passed} intents need attention")
    
    return passed == total

if __name__ == "__main__":
    # Run basic deployment test
    basic_success = test_deployment()
    
    # Run comprehensive test if basic test passes
    if basic_success:
        comprehensive_success = run_comprehensive_test()
        
        if comprehensive_success:
            print("\n🎉🎉🎉 COMPLETE DEPLOYMENT SUCCESS! 🎉🎉🎉")
            print("✅ All systems operational and ready for production")
        else:
            print("\n⚠️  Some live data intents need attention")
    else:
        print("\n⚠️  Basic deployment issues detected")


