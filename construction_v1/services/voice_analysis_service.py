# Copyright (c) 2024, Construction and contributors
# For license information, please see license.txt

import frappe
import json
import requests
from frappe.utils import get_url
from datetime import datetime

@frappe.whitelist()
def analyze_log_voice(docname):
    """
    Background job to transcribe and analyze the audio note in a Site Daily Log
    """
    try:
        doc = frappe.get_doc("Site Daily Log", docname)
        
        # 1. Get the file path
        if not doc.audio_note:
            return
            
        file_doc = frappe.get_doc("File", {"file_url": doc.audio_note})
        file_path = file_doc.get_full_path()
        
        # 2. Transcribe using Whisper (Wispr Layer)
        # In a production environment, this would call the Wispr/Whisper API
        transcription = transcribe_audio(file_path)
        
        # 3. Analyze with LLM to extract tasks and expert knowledge
        analysis_results = analyze_construction_content(transcription)
        
        # 4. Update the document
        doc.transcription = transcription
        doc.ai_summary = analysis_results.get("summary")
        doc.ai_extracted_items = json.dumps(analysis_results.get("action_items"), indent=4)
        doc.expert_knowledge_nugget = analysis_results.get("expert_knowledge")
        doc.processed_at = datetime.now()
        
        # Check if we need more info (Phase 2 feature)
        if analysis_results.get("needs_clarification"):
            doc.status = "Action Required"
            notify_superintendent(doc, analysis_results.get("clarification_questions"))
        else:
            doc.status = "Analyzed"
            
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(f"Voice Analysis Error for {docname}: {str(e)}")
        if frappe.get_all("Site Daily Log", filters={"name": docname}):
            frappe.db.set_value("Site Daily Log", docname, "status", "Draft")

def transcribe_audio(file_path):
    """
    Mock transcription service. In production, this integrates with Whisper/Wispr.
    """
    api_key = frappe.get_conf().get("whisper_api_key")
    if not api_key:
        return "Transcribed Content: [MOCK] Today we finished the slab on grade for the parking area. The concrete mix was a bit dry, so we added a superplasticizer using the incremental dosing method to maintain strength without increasing water-cement ratio. Tomorrow we move to the vertical columns."
    
    # Example API Call (Standard Whisper API)
    # response = requests.post(
    #     "https://api.openai.com/v1/audio/transcriptions",
    #     headers={"Authorization": f"Bearer {api_key}"},
    #     files={"file": open(file_path, "rb")},
    #     data={"model": "whisper-1"}
    # )
    # return response.json().get("text")
    return "[Transcription successful]"

def analyze_construction_content(text):
    """
    Uses LLM to perform construction-specific extraction
    """
    # Logic to identify:
    # - Tasks performed
    # - Future tasks (tomorrow)
    # - "How/Why" logic (expert knowledge)
    
    # Mock LLM Output
    return {
        "summary": "Completed slab on grade for parking. Managed mix consistency with superplasticizers.",
        "action_items": [
            {"task": "Cure parking slab", "date": "Tomorrow", "priority": "High"},
            {"task": "Prepare vertical columns formwork", "date": "Tomorrow", "priority": "Medium"}
        ],
        "expert_knowledge": "Used incremental dosing for superplasticizers instead of a single drop. This prevents slump loss and ensures uniform workability across the entire 40-yard pour.",
        "needs_clarification": False,
        "clarification_questions": []
    }

def notify_superintendent(doc, questions):
    """
    Trigger notifications forPhase 2: The Reviewer Bot
    """
    frappe.get_doc({
        "doctype": "Notification Log",
        "for_user": doc.superintendent,
        "subject": f"Clarification needed on Daily Log {doc.name}",
        "email_content": f"Hi {doc.superintendent}, your log mentioned a specific technique. AI has some follow-up questions: {questions[0]}",
        "document_type": "Site Daily Log",
        "document_name": doc.name
    }).insert(ignore_permissions=True)

