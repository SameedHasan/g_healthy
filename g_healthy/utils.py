"""
This file includes the utility functions
"""

import json
import re
import functools
import time
from datetime import datetime, timedelta
from dateutil import parser


import frappe


def get_request_form_data():
    """
    Returns REST API payload
    Note: Only call when payload is expected from REST API request

    Params
    ------
    NONE

    Response
    --------
    Object

    Example
    -------
    ```
    data = get_request_from_data()
    ```
    """
    if frappe.local.form_dict.data is None:
        data = frappe.safe_decode(frappe.local.request.get_data())
    else:
        data = frappe.local.form_dict.data
    try:
        return frappe.parse_json(data)
    except ValueError:
        return frappe.local.form_dict


def ensure_datetime(value):
    """
    Ensures the input value is converted to a datetime object.

    Parameters:
    value : str or datetime
        The value to be converted to a datetime object.

    Returns:
    datetime
        The converted datetime object if successful, None otherwise.
    """

    if isinstance(value, datetime):
        return value
    try:
        return parser.parse(value)
    except ValueError:
        raise ValueError(f"Invalid datetime format for value: {value}")


def ensure_uniqueness(doctype, variable, value, docname):
    """
    A function that ensures the uniqueness of the specified variable in that doctype.
    """
    if frappe.db.exists(doctype, {variable: value, "name": ["!=", docname]}):
        frappe.throw(
            f"{doctype} with {variable.replace('_', ' ')}: {value} already exists"
        )


_striptags_re = re.compile(r"(<!--.*?-->|<[^>]*>)")


def custom_strip_html(text) -> str:
    if not isinstance(text, (str, bytes)):
        # Convert non-string objects to string
        text = frappe.as_json(text) if isinstance(text, dict) else str(text)
    return _striptags_re.sub("", text)


def add_default_roles(doc, method):
    if frappe.flags.in_migrate:
        return
    # Ensure the function is executed only for DocTypes
    if doc.doctype != "DocType":
        return

    if doc.istable:
        return

    default_roles = ["System Manager", "G Healthy Admin"]  # List of roles to add

    if hasattr(doc, "permissions"):
        existing_roles = {row.role for row in doc.permissions}

        if frappe.db.exists("Role", "G Healthy Admin"):

            # Assign both roles if G Healthy Admin exists
            roles_to_assign = default_roles

            for role in roles_to_assign:
                if role not in existing_roles:
                    doc.append(
                        "permissions",
                        {"role": role, "read": 1, "write": 1, "create": 1, "delete": 1},
                    )

            doc.save()


@frappe.whitelist()
def update_docs(doctype, name, update_obj):
    """
    Updates a document in the specified doctype with the provided data.

    This function fetches the document of the given doctype and name, updates it with
    the data from the update_obj, and then saves the changes to the database.

    Parameters:
    doctype : str
        The doctype of the document to be updated.
    name : str
        The name (or ID) of the document to be updated.
    update_obj : dict
        A dictionary containing the fields and values to update in the document.

    Returns:
    None
    """
    if frappe.request.method != "PUT":
        return
    doc = frappe.get_doc(doctype, name)
    doc.update(update_obj)
    doc.save(ignore_permissions=True)
    frappe.db.commit()


def timed_execution(func):
    """Decorator to print execution time of functions."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Finished {func.__name__} in {end_time - start_time:.2f} seconds.")
        return result

    return wrapper


def cancel_and_amend(doctype, docname):
    """
    Cancel a submitted document and create a new version of the document as draft,
    copying all relevant metadata (comments, assignments, attachments, etc).
    """
    try:
        original_doc = frappe.get_doc(doctype, docname)

        if original_doc.docstatus != 1:
            return {"error": "Only submitted documents (docstatus=1) can be canceled."}

        doc_owner = original_doc.owner
        current_user = frappe.session.user

        if doc_owner != current_user:
            frappe.set_user(doc_owner)
        try:
            cancel_document(doctype, docname)
            new_doc = create_amended_doc(original_doc, docname, doc_owner)
            update_linked_docs(original_doc.doctype, original_doc.name, new_doc.name)

        except Exception as e:
            frappe.db.rollback()
            frappe.throw(f"Error while creating version: {str(e)}")

        if doc_owner != current_user:
            frappe.set_user(current_user)

        return new_doc.name

    except Exception as e:
        frappe.db.rollback()
        frappe.throw(f"Error while canceling and amending: {str(e)}")


def cancel_document(doctype, docname):
    frappe.db.set_value(doctype, docname, "docstatus", 2)
    frappe.db.commit()


def create_amended_doc(original_doc, amended_from, owner):
    new_doc = frappe.copy_doc(original_doc)
    new_doc.docstatus = 0
    new_doc.owner = owner
    new_doc.amended_from = amended_from
    # Make sure name is not same as amended_from
    if amended_from == new_doc.name:
        raise Exception(f"Name collision: new doc {new_doc.name} cannot amend itself.")

    new_doc.insert(ignore_permissions=True)

    copy_comments(original_doc.doctype, new_doc.name, amended_from)
    copy_assignments(original_doc.doctype, new_doc.name, amended_from)
    copy_shares(original_doc.doctype, new_doc.name, amended_from)
    copy_tasks(original_doc.doctype, new_doc.name, amended_from)
    frappe.db.commit()
    return new_doc


def update_linked_docs(original_doctype, original_docname, new_docname):
    """
    Update all Link fields in all doctypes that refer to the original document.
    """
    for dt in frappe.get_all("DocType", filters={"issingle": 0}):
        meta = frappe.get_meta(dt.name)
        for df in meta.fields:
            if df.fieldtype == "Link" and df.options == original_doctype:
                # Find records linking to the original doc
                records = frappe.get_all(
                    dt.name,
                    filters={
                        df.fieldname: original_docname,
                        "docstatus": ["!=", 2],
                        "name": ["!=", new_docname],
                    },
                    pluck="name",
                )
                for record in records:
                    frappe.db.set_value(dt.name, record, df.fieldname, new_docname)
    frappe.db.commit()


def copy_assignments(doctype, new_name, old_name):
    assign = frappe.db.get_value(doctype, old_name, "_assign")
    if assign:
        frappe.db.set_value(doctype, new_name, "_assign", assign)


def copy_comments(doctype, new_name, old_name):
    comments = frappe.get_all(
        "Comment",
        filters={
            "reference_doctype": doctype,
            "reference_name": old_name,
            "custom_section_reference": ["!=", ""],
            "comment_type": "Comment",
        },
        fields=["*"],
    )
    for comment_data in comments:
        try:
            frappe.db.set_value(
                "Comment", comment_data.name, "reference_name", new_name
            )
        except frappe.DoesNotExistError:
            frappe.db.rollback()
            frappe.log_error(f"Missing comment skipped during amend: {comment_data}")


def copy_tasks(doctype, new_name, old_name):
    tasks = frappe.get_all(
        "ToDo",
        filters={"reference_type": doctype, "reference_name": old_name},
        fields=["*"],
    )
    if not tasks:
        return

    meta = frappe.get_meta("ToDo")
    valid_fields = [field.fieldname for field in meta.fields] + [
        "owner",
        "creation",
        "modified",
        "modified_by",
        "docstatus",
    ]

    values = []

    for task in tasks:
        new_task = {field: task.get(field) for field in valid_fields if field in task}
        new_task["reference_name"] = new_name
        new_task["owner"] = new_task.get("owner") or frappe.session.user
        new_task["name"] = frappe.generate_hash(length=10)

        values.append(new_task)

    if values:
        frappe.db.bulk_insert(
            "ToDo",
            fields=list(values[0].keys()),
            values=[list(task.values()) for task in values],
            ignore_duplicates=True,
        )
    frappe.db.commit()


def copy_shares(doctype, new_name, old_name):
    # Make sure to fetch all necessary fields
    shares = frappe.get_all(
        "DocShare",
        fields=[
            "user",
            "share_doctype",
            "share_name",
            "read",
            "write",
            "submit",
            "share",
            "everyone",
        ],
        filters={"share_doctype": doctype, "share_name": old_name},
    )

    for share in shares:
        try:
            new_share = frappe.get_doc(
                {
                    "doctype": "DocShare",
                    "user": share.get("user"),
                    "share_doctype": share.get("share_doctype"),
                    "share_name": new_name,  # Set the new document name
                    "read": share.get("read"),
                    "write": share.get("write"),
                    "submit": share.get("submit"),
                    "share": share.get("share"),
                    "everyone": share.get("everyone"),
                }
            )
            new_share.insert(ignore_permissions=True)

        except frappe.DoesNotExistError:
            frappe.log_error(
                f"Missing share skipped during amend: {frappe.as_json(share)}"
            )


@frappe.whitelist()
def cancel_and_amend_api(doctype, docname):
    return cancel_and_amend(doctype, docname)


@frappe.whitelist()
def get_doc_versions(doctype, docname):
    """
    Returns a list of all versions of a document.
    """

    changes = frappe.db.sql(
        """
        SELECT creation, data
        FROM `tabVersion`
        WHERE ref_doctype = %s
          AND docname = %s
        ORDER BY creation
    """,
        (doctype, docname),
        as_dict=True,
    )

    return changes


from frappe.utils import now


def create_manual_version(
    doctype, docname, field_changes: list, updater_reference=None
):
    """
    Manually create a Version doc for a submitted document.

    Parameters:
    - doctype: str — Target DocType
    - docname: str — Target document name
    - field_changes: list of tuples — Format: [(fieldname, old_value, new_value)]
    - updater_reference: Optional string reference (if needed)

    Example field_changes:
        [("status", "Draft", "Under Review"), ("docstatus", 0, 1)]
    """
    version = frappe.new_doc("Version")
    version.ref_doctype = doctype
    version.docname = docname
    version.data = json.dumps(
        {
            "changed": field_changes,
            "added": [],
            "removed": [],
            "row_changed": [],
            "data_import": None,
            "updater_reference": updater_reference,
        }
    )
    version.creation = now()
    version.modified = now()
    version.owner = frappe.session.user
    version.save(ignore_permissions=True)


def update_user_sectors(doc, method):
    """
    Update the user's sectors based on user permissions,
    when a permission for Sector is added or removed.
    """
    if doc.allow != "Sector":
        return

    user = frappe.get_doc("User", doc.user)

    if method == "validate":
        if doc.for_value not in user.has_sector:
            user.append("has_sector", {"sector": doc.for_value})
    elif method == "on_trash":
        # remove matching entries safely
        user.set(
            "has_sector",
            [row for row in user.get("has_sector") if row.sector != doc.for_value],
        )

    user.save(ignore_permissions=True)
