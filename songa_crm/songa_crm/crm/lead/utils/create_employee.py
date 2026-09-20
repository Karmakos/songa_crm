def create_employee(lead):
    existing = frappe.db.get_value(
        "Employee",
        {"user_id": lead.email_id},
        "name",
    )

    if existing:
        return frappe.get_doc("Employee", existing)

    employee = frappe.get_doc({
        "doctype": "Employee",
        "first_name": lead.first_name,
        "gender": lead.gender,
        "date_of_birth": lead.date_of_birth,
        "cell_number": lead.mobile_no,
        "personal_email": lead.email_id,
    })

    employee.insert(ignore_permissions=True)

    return employee
