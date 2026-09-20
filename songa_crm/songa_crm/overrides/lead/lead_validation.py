import frappe


COMMON_FIELDS = [
    "first_name",
    "type",
    "status",
]


TYPE_FIELDS = {
    "Driver": [
        "custom_national_id_number",
        "custom_license_class",
        "custom_trike_motorcycle_experience_yrs",
        "custom_preferred_operating_zone",
        "custom_recruitment_source",
    ],

    "Farmer": [
        "custom_hub_collection_zone",
        "custom_current_buyer_off_taker",
        "custom_estimated_herd_size_cows",
        "custom_land_size_acres",
        "custom_est_daily_milk_volume_l",
        "custom_mpesa_number",
    ],

    "Cooperative": [
        "custom_member_count",
        "custom_daily_milk_collection",
        "custom_current_offtaker",
        "custom_number_of_collection_points",
        "custom_partner_area_of_operation",
    ],

    "Dairy Off-taker": [
        "custom_processing_facility_location",
        "custom_daily_intake_capacity",
        "custom_contract_type",
    ],

    "Operating Company Partner": [
        "custom_estimated_fleet_size",
        "custom_target_golive_date",
        "custom_partner_area_of_operation",
        "custom_areas_of_partnership",
    ],

    "Stakeholder": [
        "custom_stakeholder_category",
        "custom_consent_method",
        "custom_consent_optin_date",
    ],
}


VALIDATION_STATES = {
    "Contacted",
    "Engaged",
    "Onboarded",
}


def is_empty(value):
    return value is None or value == ""


def get_required_fields(doc):
    """
    Return the fields required for this Lead's Prospect Type.
    """

    required = list(COMMON_FIELDS)

    prospect_type = doc.type

    if prospect_type:
        type_fields = TYPE_FIELDS.get(prospect_type)

        if type_fields:
            required.extend(type_fields)

    return list(dict.fromkeys(required))


def validate_lead_workflow(doc, method=None):
    """
    Validate Lead before a workflow transition is saved.
    """

    # Nothing to validate if this is a new document.
    if doc.is_new():
        return

    # Get the previous workflow state from the database.
    previous_state = frappe.db.get_value(
        "Lead",
        doc.name,
        "workflow_state",
    )

    current_state = doc.workflow_state

    # No workflow transition.
    if previous_state == current_state:
        return

    # Declined and Unsubscribed do not require profile completion.
    if current_state in {"Declined", "Unsubscribed"}:
        return

    # Only enforce the full profile when entering
    # Contacted/Engaged/Onboarded.
    if current_state not in VALIDATION_STATES:
        return

    # Prospect Type is required.
    if is_empty(doc.type):
        frappe.throw(
            "Prospect Type is required before moving the Lead to "
            f"{current_state}."
        )

    # Make sure we have a validation configuration.
    type_fields = TYPE_FIELDS.get(doc.type)

    if not type_fields:
        frappe.throw(
            f"No validation configuration exists for "
            f"Prospect Type: {doc.type}"
        )

    required_fields = get_required_fields(doc)

    missing_fields = []

    for fieldname in required_fields:
        value = doc.get(fieldname)

        if is_empty(value):
            missing_fields.append(fieldname)

    if not missing_fields:
        return

    # Convert fieldnames into labels.
    meta = frappe.get_meta("Lead")

    labels = []

    for fieldname in missing_fields:
        field = meta.get_field(fieldname)

        if field:
            labels.append(field.label)
        else:
            labels.append(fieldname)

    message = (
        f"Please complete the following fields before moving "
        f"the Lead to <b>{current_state}</b>:"
        "<ul>"
        + "".join(f"<li>{frappe.utils.escape_html(label)}</li>" for label in labels)
        + "</ul>"
    )

    frappe.throw(
        message
    )
