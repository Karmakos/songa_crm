import frappe
from frappe.utils import today
from frappe.model.workflow import apply_workflow


def apply_workflow_unsubscribe_lead(lead):
    # once a lead is unsubscribed from a campaign, we will set the unsubscribed date and apply the workflow to change the status to unsubscribed.
    # Not this is not the same as unsubscribing from the email group, this is for the lead workflow.

    if lead.workflow_state == "Unsubscribed":
        return
    lead = frappe.get_doc("Lead", lead.name)

    apply_workflow(lead, "Unsubscribe")

    lead.unsubscribed = True
    lead.custom_unsubscribed_date = today()

    # Save the final state.
    lead.save(ignore_permissions=True)
