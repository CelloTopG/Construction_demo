# Copyright (c) 2024, Construction and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SiteDailyLog(Document):
    def validate(self):
        # Initial validation logic
        if not self.status:
            self.status = "Draft"

    @frappe.whitelist()
    def process_voice_note(self):
        """
        Triggered by button to start AI processing of the voice note
        """
        if not self.audio_note:
            frappe.throw("Please upload an audio note first.")
            
        self.status = "Processing"
        self.save()
        
        # Enqueue background job for transcription and analysis
        # Using background job to avoid UI timeout
        frappe.enqueue(
            "construction_v1.services.voice_analysis_service.analyze_log_voice",
            docname=self.name,
            now=frappe.flags.in_test
        )
        
        return "Voice processing started in the background."

