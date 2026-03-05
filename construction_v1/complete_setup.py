import frappe
import json

def complete_setup():
    """Complete the Construction system setup with corrected data"""
    
    print("🚀 Completing Construction system setup...")
    
    # Create corrected message templates
    create_corrected_templates()
    
    # Create sample users
    create_sample_users()
    
    # Create agent profiles with existing users
    create_agent_profiles_with_existing_users()
    
    # Test all APIs
    test_all_apis()
    
    frappe.db.commit()
    print("✅ Complete Construction system setup finished!")

def create_corrected_templates():
    """Create message templates with correct template types"""
    
    templates = [
        {
            "template_name": "Construction Payment Reminder - 30 Days",
            "template_type": "Reminder",
            "language": "en",
            "subject": "Construction Payment Due in 30 Days - Employer {employer_number}",
            "content": """Dear {employer_name},

This is a friendly reminder that your Workers' Compensation premium payment is due in 30 days.

**Payment Details:**
- Employer Number: {employer_number}
- Amount Due: K{amount_due}
- Due Date: {due_date}

**Payment Options:**
1. Online Banking Transfer
2. Bank Deposit at any Construction approved bank
3. Mobile Money (MTN, Airtel, Zamtel)
4. Visit our offices for cash payment

**Important:** Early payment helps avoid penalties and ensures continuous coverage for your employees.

Best regards,
WorkCom - Construction Virtual Assistant
Workers' Compensation Fund Control Board

For assistance, contact us:
📞 Phone: +260-XXX-XXXX
📧 Email: info@Construction.gov.zm
🌐 Website: www.Construction.gov.zm""",
            "is_active": 1
        },
        {
            "template_name": "Construction Payment Reminder - Urgent",
            "template_type": "Alert",
            "language": "en",
            "subject": "URGENT: Construction Payment Due in 7 Days - Employer {employer_number}",
            "content": """Dear {employer_name},

**URGENT REMINDER:** Your Workers' Compensation premium payment is due in 7 days.

**Payment Details:**
- Employer Number: {employer_number}
- Amount Due: K{amount_due}
- Due Date: {due_date}
- Days Remaining: 7 days

**Immediate Action Required:**
Please arrange payment immediately to avoid:
- Late payment penalties (5% of amount due)
- Suspension of coverage
- Legal action for non-compliance

**Quick Payment Options:**
- Online: www.Construction.gov.zm/payments
- Mobile Money: Dial *XXX# and follow prompts
- Bank Transfer: Account details available on our website

**Need Help?** Contact us immediately:
📞 Phone: +260-XXX-XXXX
📧 Email: payments@Construction.gov.zm

Time is running out - act now to maintain your coverage!

Best regards,
WorkCom - Construction Virtual Assistant
Workers' Compensation Fund Control Board""",
            "is_active": 1
        },
        {
            "template_name": "Construction Payment Overdue Notice",
            "template_type": "Alert",
            "language": "en",
            "subject": "OVERDUE: Construction Payment - Immediate Action Required",
            "content": """Dear {employer_name},

**PAYMENT OVERDUE NOTICE**

Your Workers' Compensation premium payment is now {days_overdue} days overdue.

**Overdue Payment Details:**
- Employer Number: {employer_number}
- Original Amount: K{amount_due}
- Days Overdue: {days_overdue}
- Original Due Date: {due_date}

**IMMEDIATE CONSEQUENCES:**
- Your workers' compensation coverage is SUSPENDED
- You are in breach of legal requirements
- Additional penalties accrue daily
- Legal action may be initiated

**URGENT ACTION REQUIRED:**
1. Pay the full amount immediately
2. Contact us to discuss payment arrangements
3. Provide proof of payment within 24 hours

**Payment Methods:**
- Emergency Hotline: +260-XXX-XXXX
- Online Payment: www.Construction.gov.zm/emergency-payment
- Visit nearest Construction office immediately

**Legal Notice:** Failure to pay within 7 days may result in legal proceedings and additional costs.

This is a serious matter requiring immediate attention.

Best regards,
WorkCom - Construction Virtual Assistant
Workers' Compensation Fund Control Board""",
            "is_active": 1
        },
        {
            "template_name": "Construction Returns Reminder",
            "template_type": "Reminder",
            "language": "en",
            "subject": "Construction Returns Submission Due - Employer {employer_number}",
            "content": """Dear {employer_name},

This is a reminder that your quarterly/annual returns submission is due in {days_remaining} days.

**Returns Details:**
- Employer Number: {employer_number}
- Return Type: {return_type}
- Period: {return_period}
- Due Date: {due_date}

**Required Documents:**
1. Employee payroll records
2. Injury/accident reports (if any)
3. Premium calculation worksheets
4. Bank payment confirmations

**Submission Methods:**
- Online Portal: www.Construction.gov.zm/returns
- Email: returns@Construction.gov.zm
- Physical submission at Construction offices
- Registered mail

**Benefits of Early Submission:**
- Avoid late submission penalties
- Faster processing and approval
- Maintain good compliance record
- Priority support for queries

Need assistance? Our returns team is ready to help you complete your submission accurately.

Best regards,
WorkCom - Construction Virtual Assistant
Workers' Compensation Fund Control Board

For assistance, contact us:
📞 Phone: +260-XXX-XXXX
📧 Email: info@Construction.gov.zm
🌐 Website: www.Construction.gov.zm""",
            "is_active": 1
        }
    ]
    
    created_count = 0
    for template_data in templates:
        try:
            if not frappe.db.exists("Message Template", template_data["template_name"]):
                template_doc = frappe.get_doc({
                    "doctype": "Message Template",
                    **template_data
                })
                template_doc.insert()
                created_count += 1
                print(f"   ✅ Created template: {template_data['template_name']}")
            else:
                print(f"   ⚠️ Template already exists: {template_data['template_name']}")
        except Exception as e:
            print(f"   ❌ Failed to create template {template_data['template_name']}: {str(e)}")
    
    print(f"📝 Created {created_count} message templates")

def create_sample_users():
    """Create sample users for agent profiles"""
    
    users = [
        {
            "email": "sarah.mwanza@Construction.gov.zm",
            "first_name": "Sarah",
            "last_name": "Mwanza",
            "enabled": 1,
            "user_type": "System User"
        },
        {
            "email": "john.banda@Construction.gov.zm", 
            "first_name": "John",
            "last_name": "Banda",
            "enabled": 1,
            "user_type": "System User"
        },
        {
            "email": "grace.phiri@Construction.gov.zm",
            "first_name": "Grace",
            "last_name": "Phiri", 
            "enabled": 1,
            "user_type": "System User"
        }
    ]
    
    created_count = 0
    for user_data in users:
        try:
            if not frappe.db.exists("User", user_data["email"]):
                user_doc = frappe.get_doc({
                    "doctype": "User",
                    **user_data
                })
                user_doc.insert()
                created_count += 1
                print(f"   ✅ Created user: {user_data['email']}")
            else:
                print(f"   ⚠️ User already exists: {user_data['email']}")
        except Exception as e:
            print(f"   ❌ Failed to create user {user_data['email']}: {str(e)}")
    
    print(f"👤 Created {created_count} users")

def create_agent_profiles_with_existing_users():
    """Create agent profiles using existing or newly created users"""
    
    # Use Administrator user as fallback
    admin_user = "Administrator"
    
    agents = [
        {
            "user": admin_user,
            "full_name": "Construction Administrator Agent",
            "skills": json.dumps(["payments", "claims", "registration", "general_support"]),
            "languages": json.dumps(["en", "bem", "ny"]),
            "experience_level": "Expert",
            "max_concurrent_conversations": 10,
            "current_workload": 0,
            "availability_status": "Available",
            "performance_rating": 5.0,
            "is_active": 1
        }
    ]
    
    # Try to add other users if they exist
    other_users = [
        ("sarah.mwanza@Construction.gov.zm", "Sarah Mwanza", "Senior", ["payments", "billing"]),
        ("john.banda@Construction.gov.zm", "John Banda", "Intermediate", ["claims", "injury_assessment"]),
        ("grace.phiri@Construction.gov.zm", "Grace Phiri", "Junior", ["registration", "compliance"])
    ]
    
    for email, name, level, skills in other_users:
        if frappe.db.exists("User", email):
            agents.append({
                "user": email,
                "full_name": name,
                "skills": json.dumps(skills),
                "languages": json.dumps(["en"]),
                "experience_level": level,
                "max_concurrent_conversations": 5,
                "current_workload": 0,
                "availability_status": "Available",
                "performance_rating": 4.5,
                "is_active": 1
            })
    
    created_count = 0
    for agent_data in agents:
        try:
            if not frappe.db.exists("Agent Profile", {"user": agent_data["user"]}):
                agent_doc = frappe.get_doc({
                    "doctype": "Agent Profile",
                    **agent_data
                })
                agent_doc.insert()
                created_count += 1
                print(f"   ✅ Created agent: {agent_data['full_name']}")
            else:
                print(f"   ⚠️ Agent already exists: {agent_data['full_name']}")
        except Exception as e:
            print(f"   ❌ Failed to create agent {agent_data['full_name']}: {str(e)}")
    
    print(f"👥 Created {created_count} agent profiles")

def test_all_apis():
    """Test all Phase 4 APIs"""
    
    print("\n🧪 Testing Phase 4 APIs...")
    
    # Test Auto-Reminder APIs
    try:
        from construction_v1.api.reminder_management import get_reminder_dashboard_data
        result = get_reminder_dashboard_data()
        if result:
            print("   ✅ Reminder Management API: Working")
        else:
            print("   ⚠️ Reminder Management API: No data returned")
    except Exception as e:
        print(f"   ❌ Reminder Management API: {str(e)}")
    
    # Test Smart Routing APIs
    try:
        from construction_v1.api.smart_routing import get_available_agents
        result = get_available_agents()
        if result:
            print("   ✅ Smart Routing API: Working")
        else:
            print("   ⚠️ Smart Routing API: No agents found")
    except Exception as e:
        print(f"   ❌ Smart Routing API: {str(e)}")
    
    # Test Predictive Analytics APIs
    try:
        from construction_v1.api.predictive_analytics import get_analytics_dashboard_data
        result = get_analytics_dashboard_data()
        if result:
            print("   ✅ Predictive Analytics API: Working")
        else:
            print("   ⚠️ Predictive Analytics API: No data returned")
    except Exception as e:
        print(f"   ❌ Predictive Analytics API: {str(e)}")
    
    print("🎯 API testing complete!")

def system_status_report():
    """Generate system status report"""
    
    print("\n" + "=" * 50)
    print("🎯 Construction SYSTEM STATUS REPORT")
    print("=" * 50)
    
    # Check DocTypes
    doctypes = ["Agent Profile", "Message Template", "Omnichannel Message", "Omnichannel Conversation"]
    for doctype in doctypes:
        exists = frappe.db.exists("DocType", doctype)
        status = "✅ Available" if exists else "❌ Missing"
        print(f"DocType {doctype}: {status}")
    
    # Check Templates
    template_count = frappe.db.count("Message Template", {"is_active": 1})
    print(f"Active Message Templates: {template_count}")
    
    # Check Agents
    agent_count = frappe.db.count("Agent Profile", {"is_active": 1})
    print(f"Active Agent Profiles: {agent_count}")
    
    # Check Services
    services = [
        "construction_v1.services.auto_reminder_service",
        "construction_v1.services.agent_skill_matching_service", 
        "construction_v1.services.predictive_analytics_service",
        "construction_v1.services.sentiment_analysis_service"
    ]
    
    for service in services:
        try:
            __import__(service)
            print(f"Service {service.split('.')[-1]}: ✅ Available")
        except Exception:
            print(f"Service {service.split('.')[-1]}: ❌ Not Available")
    
    print("\n🚀 Construction V1 System is ready for use!")
    print("📋 Next steps:")
    print("   1. Configure your specific Construction data")
    print("   2. Set up channel integrations (WhatsApp, Email, etc.)")
    print("   3. Train agents on the new system")
    print("   4. Monitor system performance")

if __name__ == "__main__":
    complete_setup()
    system_status_report()


