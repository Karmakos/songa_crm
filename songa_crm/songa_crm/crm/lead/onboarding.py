

from songa_crm.songa_crm.crm.lead.builder import (
    onboard_driver,
    onboard_farmer,
    onboard_cooperative,
    onboard_dairy_offtaker,
    onboard_operating_partner,
    onboard_stakeholder
)


def onboard_lead(doc, method=None):

    if not doc.type:
        frappe.throw(
            "Prospect Type is required to onboard a lead"
        )

    if doc.type == "Driver":
        if doc.status != "Onboarded":
            return
        onboard_driver(doc)

    elif doc.type == "Farmer":
        if doc.status != "Onboarded":
            return
        onboard_farmer(doc)

    elif doc.type == "Cooperative":
        if doc.status != "Onboarded":
            return
        onboard_cooperative(doc)

    elif doc.type == "Dairy Off-taker":
        if doc.status != "Onboarded":
            return
        onboard_dairy_offtaker(doc)

    elif doc.type == "Operating Company Partner":
        if doc.status != "Onboarded":
            return
        onboard_operating_partner(doc)

    elif doc.type == "Stakeholder":
        if doc.status not in ["To Contact", "Onboarded"]:
            return
        onboard_stakeholder(doc)

    else:
        frappe.throw(
            f"Unsupported Prospect Type: {doc.type}"
        )
