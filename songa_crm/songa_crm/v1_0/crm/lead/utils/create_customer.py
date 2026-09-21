import frappe


def create_customer(lead):
    existing = frappe.db.get_value(
        "Customer",
        {"lead_name": lead.name},
        "name",
    )

    if existing:
        return frappe.get_doc("Customer", existing)

    customer = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": lead.lead_name,
        "customer_type": "Individual",
        "email_id": lead.email_id,
        "lead_name": lead.name
    })

    customer.insert(ignore_permissions=True)

    return customer
