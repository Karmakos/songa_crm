import frappe
from songa_crm.songa_crm.v1_0.crm.lead.utils.create_employee import create_employee
from songa_crm.songa_crm.v1_0.crm.lead.utils.create_customer import create_customer
from songa_crm.songa_crm.v1_0.crm.lead.utils.create_supplier import create_supplier
from songa_crm.songa_crm.v1_0.crm.lead.utils.send_email import send_invite_to_mail_group
from songa_crm.songa_crm.v1_0.crm.lead.utils.is_subscribed import is_subscribed_to_email_group
# create onboarding functions for each prospect type

from songa_crm.songa_crm.v1_0.crm.lead.utils.unsubscribe_workflow import (
    apply_workflow_unsubscribe_lead
)


def onboard_driver(lead):

    employee = create_employee(lead)
    customer = create_customer(lead)

    # Update references
    lead.custom_customer_name = customer.name
    lead.custom_supplier_name = employee.name

    return {
        "employee": employee.name,
        "customer": customer.name,
    }


def onboard_farmer(lead):
    customer = create_customer(lead)
    supplier = create_supplier(lead)

    # create farmer group to be added
    lead.custom_customer_name = customer.name
    lead.custom_supplier_name = supplier.name

    return {
        "customer": customer.name,
        "supplier": supplier.name,
    }


def onboard_cooperative(lead):
    customer = create_customer(lead)
    supplier = create_supplier(lead)

    # Update back references to lead
    lead.custom_customer_name = customer.name
    lead.custom_supplier_name = supplier.name

    return {
        "customer": customer.name,
        "supplier": supplier.name,
    }


def onboard_dairy_offtaker(lead):
    customer = create_customer(lead)

    # Update back references
    lead.custom_customer_name = customer.name

    return {
        "customer": customer.name
    }


def onboard_operating_partner(lead):

    customer = create_customer(lead)

    # erp provisioning to be defined

    # Update back to references
    lead.custom_customer_name = customer.name

    return {
        "customer": customer.name
    }


def onboard_stakeholder(lead):

    # add to email group
    if lead.status == "To Contact":
        send_invite_to_mail_group(lead)

    # check if lead is subscribed to email group
    if lead.status == "Engaged":
        is_subscribed_to_email_group(lead)
