def create_supplier(lead):
    existing = frappe.db.get_value(
        "Supplier",
        {
            "supplier_name": lead.lead_name,
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
