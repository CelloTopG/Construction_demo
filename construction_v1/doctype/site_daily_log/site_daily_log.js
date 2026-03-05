# Copyright(c) 2024, Construction and contributors
# For license information, please see license.txt

frappe.ui.form.on('Site Daily Log', {
    refresh: function (frm) {
        if (frm.doc.audio_note && frm.doc.status === "Draft") {
            frm.add_custom_button(__('Process Voice Recording'), function () {
                frm.call('process_voice_note').then(r => {
                    frappe.msgprint(r.message);
                    frm.reload_doc();
                });
            }).addClass("btn-primary");
        }

        if (frm.doc.status === "Processing") {
            frm.dashboard.set_headline(__('AI is currently analyzing this log. Please wait...'));
            // Auto-reload every 15 seconds while processing
            setTimeout(() => {
                frm.reload_doc();
            }, 15000);
        }
    },

    process_voice: function (frm) {
        frm.trigger('process_voice_note');
    }
});

