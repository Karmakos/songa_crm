import frappe
from frappe.utils.data import cstr


def is_subscribed_to_email_group(lead):
    if not lead.type or not lead.email_id:
        return

    email_group = cstr(lead.type) + " Newsletter"

    exists = frappe.db.exists(

        "Email Group Member",
        {
            "email_group": email_group,
            "email": lead.email_id,
        },
    )

    if not exists:
        frappe.throw(
            f'''Lead {lead.name} is not subscribed to the {email_group} email group. 
            You cannot Onboard this lead until they are subscribed. Please contact the lead and request their consent to subscribe before onboarding them. '''
        )
