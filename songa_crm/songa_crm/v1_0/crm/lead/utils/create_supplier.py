import frappe


def create_supplier(lead):
    existing = frappe.db.get_value(
        "Supplier",
        {
            "custom_lead_name": lead.name,
        },
        "name",
    )

    if existing:
        return frappe.get_doc("Supplier", existing)

    supplier = frappe.get_doc({
        "doctype": "Supplier",
        "supplier_name": lead.lead_name,
        "supplier_type": "Individual",
    })

    supplier.insert(ignore_permissions=True)

    return supplier
