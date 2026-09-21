import frappe
from frappe.email.doctype.newsletter.newsletter import subscribe
from frappe.utils import cstr


def send_invite_to_mail_group(lead):

    if not lead.type:
        return

    email_group = cstr(lead.type) + " Newsletter"

    existing = frappe.db.get_value(
        "Email Group",
        {
            "name": email_group,
        },
        "name",
    )

    if not existing:
        frappe.get_doc({
            "doctype": "Email Group",
            "name": email_group,
        }).insert(ignore_permissions=True)

    subscribe(
        email=lead.email_id,
        email_group=email_group
    )
