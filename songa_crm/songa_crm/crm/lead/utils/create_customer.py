def create_customer(lead):
    existing = frappe.db.get_value(
        "Customer",
        {"customer_name": lead.lead_name},
        "name",
    )

    if existing:
        return frappe.get_doc("Customer", existing)

    customer = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": lead.lead_name,
        "customer_type": "Individual",
    })

    customer.insert(ignore_permissions=True)

    return customer
