import frappe

from songa_crm.songa_crm.v1_0.crm.lead.builder import (
    onboard_driver,
    onboard_farmer,
    onboard_cooperative,
    onboard_dairy_offtaker,
    onboard_operating_partner,
    onboard_stakeholder
)
from songa_crm.songa_crm.v1_0.crm.lead.utils.unsubscribe_workflow import apply_workflow_unsubscribe_lead


def onboard_lead(doc, method=None):
    try:
        if not doc.type:
            frappe.throw(
                "Prospect Type is required to onboard a lead"
            )

        # Prioritize unsubscribed updates
        if doc.unsubscribed:

            apply_workflow_unsubscribe_lead(doc)

        if doc.type == "Driver":
            if doc.workflow_state != "Onboarded":
                return
            onboard_driver(doc)

        elif doc.type == "Farmer":
            if doc.workflow_state != "Onboarded":
                return
            onboard_farmer(doc)

        elif doc.type == "Cooperative":
            if doc.workflow_state != "Onboarded":
                return
            onboard_cooperative(doc)

        elif doc.type == "Dairy Off-taker":
            if doc.workflow_state != "Onboarded":
                return
            onboard_dairy_offtaker(doc)

        elif doc.type == "Operating Company Partner":
            if doc.workflow_state != "Onboarded":
                return
            onboard_operating_partner(doc)

        elif doc.type == "Stakeholder":

            if doc.workflow_state in ["To Contact", "Engaged"]:
                onboard_stakeholder(doc)

        else:
            frappe.throw(
                f"Unsupported Prospect Type: {doc.type}"
            )

    except Exception:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Lead onboarding failed",
        )
        frappe.throw(
            msg=("There was an issue processing your request. Please contact support!"),
            title=("Invalid Onboarding Data"),
            exc=frappe.ValidationError
        )
