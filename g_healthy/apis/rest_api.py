import json

import frappe
import frappe.share
from frappe import _
from frappe.desk.form.assign_to import (
    format_message_for_assign_to,
    get,
    notify_assignment,
)
from frappe.desk.form.document_follow import follow_document
from frappe.utils.data import strip_html


@frappe.whitelist()
def todo_before_insert(doc, method):
    if not doc.description:
        doc.description = doc.custom_remarks


@frappe.whitelist()
def override_share_add(args=None, *, ignore_permissions=False):
    """add in someone's to do list
    args = {
                    "assign_to": [],
                    "doctype": ,
                    "name": ,
                    "description": ,
                    "assignment_rule":
    }

    """
    if not args:
        args = frappe.local.form_dict

    users_with_duplicate_todo = []
    shared_with_users = []

    for assign_to in frappe.parse_json(args.get("assign_to")):
        filters = {
            "reference_type": args["doctype"],
            "reference_name": args["name"],
            "status": "Open",
            "custom_workflow_status": args["custom_workflow_status"],
            "allocated_to": assign_to,
        }
        if not ignore_permissions:
            frappe.get_doc(args["doctype"], args["name"]).check_permission()

        from frappe.utils import nowdate

        description = str(args.get("description", ""))
        has_content = strip_html(description) or "<img" in description
        if not has_content:
            args["description"] = _("Assignment for {0} {1}").format(
                args["doctype"], args["name"]
            )
        d = frappe.get_doc(
            {
                "doctype": "ToDo",
                "allocated_to": assign_to,
                "reference_type": args["doctype"],
                "reference_name": args["name"],
                "description": args["custom_remarks"],
                "custom_remarks": args["custom_remarks"],
                "priority": args.get("priority", "Medium"),
                "status": "Open",
                "custom_workflow_status": args["custom_workflow_status"],
                "date": args.get("custom_assigned_date", nowdate()),
                "assigned_by": args.get("assigned_by", frappe.session.user),
                "assignment_rule": args.get("assignment_rule"),
            }
        ).insert(ignore_permissions=True)

        # set assigned_to if field exists
        if frappe.get_meta(args["doctype"]).get_field("assigned_to"):
            frappe.db.set_value(args["doctype"], args["name"], "assigned_to", assign_to)
        # doc = frappe.get_doc(args["doctype"], args["name"])
        # doc.workflow_initiated = 1
        # doc.last_assigned_to = assign_to
        # doc.save(ignore_permissions=True)
        # frappe.db.commit()
        frappe.share.add(
            args["doctype"],
            args["name"],
            assign_to,
            read=1,
            write=1,
            submit=0,
            share=1,
            everyone=0,
            notify=0,
        )
        shared_with_users.append(assign_to)
        doc_meta = frappe.get_meta(args["doctype"])

        # make this document followed by assigned user
        if frappe.get_cached_value("User", assign_to, "follow_assigned_documents"):
            follow_document(args["doctype"], args["name"], assign_to)

        # notify
        notify_assignment(
            d.assigned_by,
            d.allocated_to,
            d.reference_type,
            d.reference_name,
            action="ASSIGN",
            description=args.get("description"),
        )

    if shared_with_users:
        user_list = format_message_for_assign_to(shared_with_users)
        frappe.msgprint(
            _("Shared with the following Users:{0}").format(user_list, alert=True)
        )

    if users_with_duplicate_todo:
        user_list = format_message_for_assign_to(users_with_duplicate_todo)
        frappe.msgprint(
            _("Already in the following Users ToDo list:{0}").format(
                user_list, alert=True
            )
        )

    return get(args)


@frappe.whitelist()
def get_changed_fields(doctype, docname, fieldname=None, order="asc"):
    """
    Retrieve the changed fields for a specific document from the Version table.
    If a specific fieldname is provided, return changes only for that field.
    Supports ordering by timestamp (asc or desc).
    """
    try:
        order_by = "creation asc" if order.lower() == "asc" else "creation desc"

        versions = frappe.get_all(
            "Version",
            filters={"ref_doctype": doctype, "docname": docname},
            fields=["data", "creation", "modified_by"],
            order_by=order_by,
        )

        changes = []
        fieldname = fieldname.strip() if fieldname else None

        for version in versions:
            version_data = json.loads(version["data"])

            if "changed" in version_data:
                for field_change in version_data["changed"]:
                    field, old_value, new_value = field_change

                    if fieldname and field != fieldname:
                        continue
                    meta = frappe.get_meta(doctype)
                    if not meta.get_field(field):
                        continue

                    if meta.get_field(field).get("fieldtype") in {
                        "Data",
                        "Small Text",
                        "Text",
                        "Long Text",
                        "Link",
                        "Select",
                        "Code",
                        "Markdown",
                    }:
                        old_value = (old_value or "").strip()
                        new_value = (new_value or "").strip()
                    elif meta.get_field(field).get("fieldtype") in {
                        "Float",
                        "Currency",
                        "Percent",
                    }:
                        old_value = (
                            float(old_value) if old_value not in (None, "") else 0.0
                        )
                        new_value = (
                            float(new_value) if new_value not in (None, "") else 0.0
                        )
                    elif meta.get_field(field).get("fieldtype") in {"Int", "Check"}:
                        old_value = int(old_value) if old_value not in (None, "") else 0
                        new_value = int(new_value) if new_value not in (None, "") else 0
                    else:
                        old_value, new_value = old_value, new_value

                    if old_value == new_value or (not old_value and not new_value):
                        continue

                    fieldtype = meta.get_field(field).get("fieldtype")
                    link_doctype = meta.get_field(field).get("options")

                    field_to_fetch = "name"

                    if fieldtype == "Link" and link_doctype:
                        try:
                            linked_meta = frappe.get_meta(link_doctype)
                            field_to_fetch = linked_meta.title_field or "name"
                        except Exception:
                            field_to_fetch = "name"

                        if old_value:
                            old_value = frappe.db.get_value(
                                link_doctype, old_value, field_to_fetch
                            )
                        if new_value:
                            new_value = frappe.db.get_value(
                                link_doctype, new_value, field_to_fetch
                            )

                    changes.append(
                        {
                            "label": meta.get_label(field),
                            "field": field,
                            "old_value": old_value,
                            "new_value": new_value,
                            "timestamp": version["creation"],
                            "modified_by": version["modified_by"],
                        }
                    )

        return changes
    except Exception as e:
        frappe.throw(str(e))
