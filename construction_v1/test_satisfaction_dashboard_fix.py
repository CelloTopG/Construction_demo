#!/usr/bin/env python3
"""
Test Satisfaction Dashboard Fix
"""

import frappe
from frappe import _
from datetime import datetime

def test_satisfaction_dashboard_fix():
    """Test the satisfaction dashboard fix"""
    
    print("🔧 TESTING SATISFACTION DASHBOARD FIX")
    print("=" * 60)
    
    test_results = {
        "dashboard_function_works": False,
        "returns_valid_data": False,
        "no_errors": False,
        "data_structure_correct": False,
        "error_details": None
    }
    
    try:
        # Test 1: Basic function execution
        print("\n🧪 Test 1: Basic Function Execution")
        from construction_v1.api.sentiment_analysis import get_satisfaction_dashboard
        
        result = get_satisfaction_dashboard()
        
        if result.get("status") == "success":
            print("✅ Dashboard function executed successfully")
            test_results["dashboard_function_works"] = True
            test_results["no_errors"] = True
        else:
            print(f"❌ Dashboard function failed: {result.get('message', 'Unknown error')}")
            test_results["error_details"] = result.get("details", result.get("message", "Unknown error"))
            return test_results
        
        # Test 2: Data structure validation
        print("\n📊 Test 2: Data Structure Validation")
        dashboard_data = result.get("dashboard_data", {})
        
        required_keys = [
            "total_interactions",
            "average_sentiment", 
            "sentiment_distribution",
            "emotion_distribution",
            "satisfaction_trend",
            "alerts_summary",
            "top_negative_users",
            "period"
        ]
        
        missing_keys = []
        for key in required_keys:
            if key in dashboard_data:
                print(f"✅ {key}: Present")
            else:
                print(f"❌ {key}: Missing")
                missing_keys.append(key)
        
        if len(missing_keys) == 0:
            print("✅ All required data keys present")
            test_results["data_structure_correct"] = True
        else:
            print(f"❌ Missing keys: {missing_keys}")
        
        # Test 3: Data content validation
        print("\n🔍 Test 3: Data Content Validation")
        
        total_interactions = dashboard_data.get("total_interactions", 0)
        average_sentiment = dashboard_data.get("average_sentiment", 0)
        
        print(f"📈 Total Interactions: {total_interactions}")
        print(f"🎭 Average Sentiment: {average_sentiment}")
        
        # Check if data types are correct
        if isinstance(total_interactions, int) and isinstance(average_sentiment, (int, float)):
            print("✅ Data types are correct")
            test_results["returns_valid_data"] = True
        else:
            print("❌ Data types are incorrect")
        
        # Test 4: Helper functions
        print("\n🔧 Test 4: Helper Functions")
        try:
            from construction_v1.api.sentiment_analysis import (
                calculate_sentiment_distribution,
                calculate_emotion_distribution,
                calculate_satisfaction_trend,
                get_recent_alerts,
                get_users_needing_attention
            )
            
            # Test with sample data
            sample_scores = [0.5, -0.3, 0.8, -0.1, 0.2]
            sentiment_dist = calculate_sentiment_distribution(sample_scores)
            print(f"✅ Sentiment Distribution: {sentiment_dist}")
            
            # Test with empty data
            empty_dist = calculate_sentiment_distribution([])
            print(f"✅ Empty Sentiment Distribution: {empty_dist}")
            
            alerts = get_recent_alerts()
            print(f"✅ Recent Alerts: {alerts}")
            
        except Exception as e:
            print(f"❌ Helper function error: {str(e)}")
            test_results["error_details"] = f"Helper function error: {str(e)}"
        
        # Test 5: Create sample data and retest
        print("\n📝 Test 5: Testing with Sample Data")
        try:
            # Create a sample interaction if none exist
            if total_interactions == 0:
                print("Creating sample interaction for testing...")
                create_sample_interaction()
                
                # Retest dashboard
                result2 = get_satisfaction_dashboard()
                if result2.get("status") == "success":
                    new_total = result2.get("dashboard_data", {}).get("total_interactions", 0)
                    print(f"✅ Dashboard works with sample data: {new_total} interactions")
                else:
                    print(f"❌ Dashboard failed with sample data: {result2.get('message')}")
            else:
                print(f"✅ Dashboard working with existing data: {total_interactions} interactions")
        
        except Exception as e:
            print(f"❌ Sample data test error: {str(e)}")
        
        # Generate final assessment
        generate_fix_assessment(test_results)
        
        return test_results
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR during testing: {str(e)}")
        test_results["error_details"] = str(e)
        return test_results

def create_sample_interaction():
    """Create a sample interaction for testing"""
    try:
        interaction = frappe.new_doc("User Interaction Log")
        interaction.user_id = "test_dashboard_user"
        interaction.query_text = "Test query for dashboard"
        interaction.response_provided = "Test response"
        interaction.satisfaction_rating = 4
        interaction.timestamp = frappe.utils.now()
        interaction.session_id = "test_dashboard_session"
        interaction.confidence_score = 0.8
        
        # Add ML fields if they exist
        if hasattr(interaction, "ml_sentiment_score"):
            interaction.ml_sentiment_score = 0.6
        if hasattr(interaction, "ml_emotion_detected"):
            interaction.ml_emotion_detected = "satisfied"
        
        interaction.insert()
        frappe.db.commit()
        print("✅ Sample interaction created")
        
    except Exception as e:
        print(f"❌ Failed to create sample interaction: {str(e)}")

def generate_fix_assessment(test_results):
    """Generate assessment of the fix"""
    
    print("\n" + "=" * 60)
    print("🔬 FIX ASSESSMENT RESULTS")
    print("=" * 60)
    
    passed_tests = sum(1 for result in test_results.values() if result is True)
    total_tests = len([k for k in test_results.keys() if k != "error_details"])
    
    print(f"📊 Tests Passed: {passed_tests}/{total_tests}")
    print(f"✅ Dashboard Function Works: {'YES' if test_results['dashboard_function_works'] else 'NO'}")
    print(f"📋 Returns Valid Data: {'YES' if test_results['returns_valid_data'] else 'NO'}")
    print(f"❌ No Errors: {'YES' if test_results['no_errors'] else 'NO'}")
    print(f"🏗️ Data Structure Correct: {'YES' if test_results['data_structure_correct'] else 'NO'}")
    
    if test_results["error_details"]:
        print(f"\n🔍 Error Details: {test_results['error_details']}")
    
    # Overall assessment
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if success_rate == 100:
        print("   🎉 PERFECT - Fix completely successful!")
        print("   ✅ All tests passed")
        print("   🚀 Dashboard ready for production")
    elif success_rate >= 75:
        print("   ✅ GOOD - Fix mostly successful!")
        print("   🎯 Most functionality working")
        print("   🔧 Minor issues may remain")
    elif success_rate >= 50:
        print("   🟡 PARTIAL - Fix partially successful")
        print("   📋 Some functionality working")
        print("   🔧 Additional fixes needed")
    else:
        print("   ❌ FAILED - Fix unsuccessful")
        print("   🔧 Major issues remain")
        print("   📋 Requires further investigation")
    
    return success_rate

def run_specific_dashboard_test():
    """Run the specific test that was failing"""
    
    print("\n🎯 RUNNING SPECIFIC FAILING TEST")
    print("-" * 40)
    
    try:
        from construction_v1.api.sentiment_analysis import get_satisfaction_dashboard
        
        result = get_satisfaction_dashboard()
        
        if result.get("status") == "success":
            print("✅ Satisfaction Dashboard Test: PASSED")
            dashboard_data = result.get("dashboard_data", {})
            print(f"   📊 Total Interactions: {dashboard_data.get('total_interactions', 0)}")
            print(f"   🎭 Average Sentiment: {dashboard_data.get('average_sentiment', 0)}")
            print(f"   📈 Data Quality: {dashboard_data.get('data_quality', {})}")
            return True
        else:
            print("❌ Satisfaction Dashboard Test: FAILED")
            print(f"   Error: {result.get('message', 'Unknown error')}")
            print(f"   Details: {result.get('details', 'No details')}")
            return False
            
    except Exception as e:
        print("❌ Satisfaction Dashboard Test: ERROR")
        print(f"   Exception: {str(e)}")
        return False

if __name__ == "__main__":
    frappe.init(site="dev")
    frappe.connect()
    
    # Run comprehensive fix testing
    results = test_satisfaction_dashboard_fix()
    
    # Run specific test
    specific_test_passed = run_specific_dashboard_test()
    
    print(f"\n🏁 FINAL RESULT:")
    if specific_test_passed:
        print("🎉 SATISFACTION DASHBOARD FIX: SUCCESS!")
        print("✅ The failing test now passes")
        print("🚀 Ready for Phase 4 re-testing")
    else:
        print("❌ SATISFACTION DASHBOARD FIX: STILL FAILING")
        print("🔧 Additional investigation needed")
    
    print("=" * 60)

