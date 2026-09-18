import frappe


WORKFLOW_NAME = "Songa Lead Workflow"
DOCTYPE = "Lead"


STATES = [
    {
        "state": "Identified",
        "doc_status": 0,
        "update_field": "status",
        "update_value": "Identified",
        "allow_edit": "Sales User",
    },
    {
        "state": "To Contact",
        "doc_status": 0,
        "update_field": "status",
        "update_value": "To Contact",
        "allow_edit": "Sales User",
    },
    {
        "state": "Contacted",
        "doc_status": 0,
        "update_field": "status",
        "update_value": "Contacted",
        "allow_edit": "Sales User",
    },
    {
        "state": "Engaged",
        "doc_status": 0,
        "update_field": "status",
        "update_value": "Engaged",
        "allow_edit": "Sales User",
    },
    {
        "state": "Onboarded",
        "doc_status": 0,
        "update_field": "status",
        "update_value": "Onboarded",
        "allow_edit": "Sales User",
    },
    {
        "state": "Declined",
        "doc_status": 0,
        "update_field": "status",
        "update_value": "Declined",
        "allow_edit": "Sales User",
    },
]


TRANSITIONS = [
    {
        "state": "Identified",
        "action": "Move to Contact",
        "next_state": "To Contact",
        "allowed": "Sales User",
    },
    {
        "state": "To Contact",
        "action": "Mark Contacted",
        "next_state": "Contacted",
        "allowed": "Sales User",
    },
    {
        "state": "Contacted",
        "action": "Mark Engaged",
        "next_state": "Engaged",
        "allowed": "Sales User",
    },
    {
        "state": "Engaged",
        "action": "Approve Onboarding",
        "next_state": "Onboarded",
        "allowed": "Sales Manager",
    },
    {
        "state": "Identified",
        "action": "Decline",
        "next_state": "Declined",
        "allowed": "Sales User",
    },
    {
        "state": "To Contact",
        "action": "Decline",
        "next_state": "Declined",
        "allowed": "Sales User",
    },
    {
        "state": "Contacted",
        "action": "Decline",
        "next_state": "Declined",
        "allowed": "Sales User",
    },
    {
        "state": "Engaged",
        "action": "Decline",
        "next_state": "Declined",
        "allowed": "Sales User",
    },
    {
        "state": "Declined",
        "action": "Reopen",
        "next_state": "Engaged",
        "allowed": "Sales Manager",
    },
]


def execute():
    create_workflow_states()
    create_workflow_action_masters()
    workflow = get_or_create_workflow()

    sync_states(workflow)
    sync_transitions(workflow)

    workflow.save(ignore_permissions=True)


def create_workflow_states():
    for state in STATES:
        state_name = state["state"]

        if frappe.db.exists("Workflow State", state_name):
            continue

        frappe.get_doc({
            "doctype": "Workflow State",
            "workflow_state_name": state_name,
        }).insert(ignore_permissions=True)


def create_workflow_action_masters():
    actions = {
        transition["action"]
        for transition in TRANSITIONS
    }

    for action_name in actions:
        if frappe.db.exists("Workflow Action Master", action_name):
            continue

        frappe.get_doc({
            "doctype": "Workflow Action Master",
            "workflow_action_name": action_name,
        }).insert(ignore_permissions=True)


def get_or_create_workflow():
    if frappe.db.exists("Workflow", WORKFLOW_NAME):
        workflow = frappe.get_doc("Workflow", WORKFLOW_NAME)
    else:
        workflow = frappe.new_doc("Workflow")
        workflow.workflow_name = WORKFLOW_NAME

    workflow.document_type = DOCTYPE
    workflow.workflow_state_field = "workflow_state"
    workflow.is_active = 1
    workflow.send_email_alert = 0

    return workflow


def sync_states(workflow):
    existing = {
        row.state: row
        for row in workflow.states
    }

    for state in STATES:
        row = existing.get(state["state"])

        if row:
            row.doc_status = state["doc_status"]
        else:
            workflow.append(
                "states",
                {
                    "state": state["state"],
                    "doc_status": state["doc_status"],
                    "update_field": state["update_field"],
                    "update_value": state["update_value"],
                    "allow_edit": state["allow_edit"],
                },
            )


def sync_transitions(workflow):
    desired = {
        (
            transition["state"],
            transition["action"],
            transition["next_state"],
            transition["allowed"],
        )
        for transition in TRANSITIONS
    }

    # Remove transitions nott defined by applicaop
    workflow.transitions = [
        row
        for row in workflow.transitions
        if (
            row.state,
            row.action,
            row.next_state,
            row.allowed,
        ) in desired
    ]

    existing = {
        (
            row.state,
            row.action,
            row.next_state,
            row.allowed,
        )
        for row in workflow.transitions
    }

    for transition in TRANSITIONS:
        key = (
            transition["state"],
            transition["action"],
            transition["next_state"],
            transition["allowed"],
        )

        if key in existing:
            continue

        workflow.append(
            "transitions",
            {
                "state": transition["state"],
                "action": transition["action"],
                "next_state": transition["next_state"],
                "allowed": transition["allowed"],
            },
        )
