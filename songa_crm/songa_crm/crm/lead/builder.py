import frappe
from songa_crm.songa_crm.crm.lead.utils.create_employee import create_employee
from songa_crm.songa_crm.crm.lead.utils.create_customer import create_customer

# create onboarding functions for each prospect type


def onboard_driver(lead):

    employee = create_employee(lead)
    customer = create_customer(lead)

    return {
        "employee": employee.name,
        "customer": customer.name,
    }


def onboard_farmer(lead):
    customer = ensure_farmer_customer(lead)
    supplier = ensure_farmer_supplier(lead)
    farmer_group = ensure_farmer_group(lead)

    return {
        "customer": customer.name,
        "supplier": supplier.name,
        "farmer_group": farmer_group.name,
    }


def onboard_cooperative(lead):
    customer = ensure_farmer_customer(lead)
    supplier = ensure_farmer_supplier(lead)

    return {
        "customer": customer.name,
        "supplier": supplier.name,
    }


def onboard_dairy_offtaker(lead):
    customer = ensure_farmer_customer(lead)

    return {
        "customer": customer.name
    }


def onboard_operating_partner(lead):

    customer = ensure_farmer_customer(lead)
    # erp provisioning to be defined

    return {
        "customer": customer.name
    }


def onboard_stakeholder(lead):
    # adding to email group to be defined
    pass
