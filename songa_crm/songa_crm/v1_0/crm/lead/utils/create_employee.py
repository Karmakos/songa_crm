import frappe
from frappe.utils import today


def create_employee(lead):
    existing = frappe.db.get_value(
        "Employee",
        {
            "custom_lead_name": lead.name
        },
        "name",
    )

    if existing:
        return frappe.get_doc("Employee", existing)

    employee = frappe.get_doc({
        "doctype": "Employee",
        "first_name": lead.first_name,
        "gender": lead.gender,
        "date_of_birth": lead.custom_date_of_birth,
        "date_of_joining": today(),
        "cell_number": lead.mobile_no,
        "personal_email": lead.email_id,
    })

    employee.insert(ignore_permissions=True)

    return employee
