frappe.ui.form.on("Lead", {
    refresh(frm) {
        const workflow_state = frm.doc.workflow_state;

        // Reset field-level read-only properties first.
        frm.set_df_property("type", "read_only", 0);
        frm.set_df_property("status", "read_only", 0);
        frm.set_df_property("request_type", "read_only", 0);

        // lock selected fields on engaged.
        if (workflow_state === "Engaged") {
            frm.set_df_property("type", "read_only", 1);
            frm.set_df_property("status", "read_only", 1);
            frm.set_df_property("request_type", "read_only", 1);
        }

        // Terminal states locks the entire form.
        if (["Unsubscribed", "Onboarded", "Declined"].includes(workflow_state)) {
            frm.disable_form();
        }
    }
});