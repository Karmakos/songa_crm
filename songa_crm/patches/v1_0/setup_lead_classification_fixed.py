
import frappe
from frappe.custom.doctype.property_setter.property_setter import (
    make_property_setter,
)


def execute():
    configure_lead_classification()


def configure_lead_classification():
    fields = [
        {
            "field": "status",
            "options": [
                "Identified",
                "To Contact",
                "Contacted",
                "Engaged",
                "Onboarded",
                "Declined",
            ],
            "default": "Identified",
        },
        {
            "field": "type",
            "options": [
                "",
                "Driver",
                "Farmer",
                "Cooperative",
                "Dairy Off-taker",
                "Operating Company Partner",
                "Stakeholder",
            ],
            "default": "",
        },
        {
            "field": "request_type",
            "options": [
                "",
                "Driver Recruitment",
                "Farmer Onboarding",
                "Cooperative Partnership",
                "Dairy Off-taker Partnership",
                "Operating Partnership",
                "Stakeholder Engagement",
                "Other",
            ],
            "default": "",
        },
    ]

    for field in fields:
        make_property_setter(
            "Lead",
            field["field"],
            "options",
            "\n".join(field["options"]),
            "Text",
            validate_fields_for_doctype=False,
        )

        make_property_setter(
            "Lead",
            field["field"],
            "default",
            field.get("default"),
            "data",
            validate_fields_for_doctype=False,
        )
