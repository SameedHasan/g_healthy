import os
from mimetypes import guess_type

import frappe
from frappe import _
from frappe.handler import ALLOWED_MIMETYPES, check_write_permission
from frappe.utils import cint
from frappe.utils.file_manager import save_file
from frappe.utils.image import optimize_image
from werkzeug.utils import secure_filename


@frappe.whitelist()
def upload_document():
    if "file" not in frappe.request.files:
        frappe.throw(_("No file provided"))

    uploaded_file = frappe.request.files["file"]
    job = frappe.form_dict.get("job")
    file_content = uploaded_file.read()

    added_by = frappe.session.user
    user_info = frappe.get_doc("User", added_by)
    new_document = frappe.get_doc(
        {
            "doctype": "Documents",
            "file_name": uploaded_file.filename,
            "date": frappe.utils.now_datetime(),
            "size": str(round(len(file_content) / (1024.0 * 1024.0))) + " Mbs",
            "added_by": user_info.full_name,
            "file_extension": os.path.splitext(uploaded_file.filename)[1],
            "jobs": job,
        }
    ).insert()
    saved_file = save_file(
        fname=uploaded_file.filename,
        content=file_content,
        dt="Documents",
        dn=new_document.name,
    )
    new_document.file_url = saved_file.file_url
    new_document.save()
    frappe.get_doc(
        {
            "doctype": "Activities",
            "type": "Documents",
            "user": user_info.full_name,
            "activity": "uploaded new document to job: " + job,
            "tags": '{"tags": ["' + uploaded_file.filename + '"]}',
            "jobs": job,
        }
    ).insert(ignore_permissions=True)
    frappe.db.commit()
    return _("File uploaded successfully")


def add_activity_log(
    activity_type, activity_description, file_name=None, job=None, cargo_details=None
):
    """
    Adds an Activity record against specified document.

    Args:a
        activity_type (str): The type of activity being logged.
        activity_description (str): A description of the activity being performed.
        file_name (str, optional): The name of the file associated with the activity.
        job (str, optional): The job associated with the activity. Defaults to None.
        cargo_details (str, optional): The cargo details associated with the activity.

    Returns:
        None

    Raises:
        None
    """
    added_by = frappe.session.user
    user_info = frappe.get_doc("User", added_by)
    user_full_name = (user_info.full_name,)
    tags = '{"tags": ["' + file_name + '"]}' if file_name else None
    doc = frappe.get_doc(
        {
            "doctype": "Activities",
            "type": activity_type,
            "user": user_full_name,
            "activity": activity_description,
            "tags": tags,
        }
    )
    if job:
        doc.jobs = job

    if cargo_details:
        doc.cargo_details = cargo_details
    doc.insert(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def upload_multiple_files():
    user = None
    if frappe.session.user == "Guest":
        if frappe.get_system_settings("allow_guests_to_upload_files"):
            ignore_permissions = True
        else:
            raise frappe.PermissionError
    else:
        user = frappe.get_doc("User", frappe.session.user)
        ignore_permissions = False

    files = frappe.request.files.getlist("files")
    is_private = cint(frappe.form_dict.get("is_private", 0))
    doctype = frappe.form_dict.get("doctype")
    docname = frappe.form_dict.get("docname")
    file_url = frappe.form_dict.file_url
    fieldname = frappe.form_dict.fieldname
    is_annexure = cint(frappe.form_dict.get("is_annexure", 0))
    custom_annexure_number = frappe.form_dict.get("annexure_number")
    custom_attached_to_section = frappe.form_dict.get("attached_to_section")
    folder = frappe.form_dict.get("folder", "Home")
    optimize = frappe.form_dict.get("optimize")
    custom_type_of_document = frappe.form_dict.get("custom_type_of_document")
    approval_type = frappe.form_dict.get("approval_type")
    approved_date = frappe.form_dict.get("date")
    custom_title_of_document = frappe.form_dict.get("custom_title_of_document")
    custom_date = frappe.form_dict.get("custom_date")

    if not doctype or not docname:
        frappe.throw(_("doctype and docname are required fields."))

    uploaded_files = []

    for file in files:
        filename = secure_filename(file.filename)
        content = file.stream.read()
        content_type = guess_type(filename)[0]

        if not ignore_permissions:
            check_write_permission(doctype, docname)

        if content_type not in ALLOWED_MIMETYPES:
            frappe.throw(
                _(
                    "You can only upload JPG, PNG, PDF, TXT, CSV, or Microsoft documents."
                )
            )

        if optimize and content_type and content_type.startswith("image/"):
            args = {"content": content, "content_type": content_type}
            if frappe.form_dict.get("max_width"):
                args["max_width"] = int(frappe.form_dict["max_width"])
            if frappe.form_dict.get("max_height"):
                args["max_height"] = int(frappe.form_dict["max_height"])
            content = optimize_image(**args)

        file_doc = frappe.get_doc(
            {
                "doctype": "File",
                "attached_to_doctype": doctype,
                "attached_to_name": docname,
                "attached_to_field": fieldname,
                "file_url": file_url,
                "folder": folder,
                "custom_is_annexure": is_annexure,
                "custom_annexure_number": custom_annexure_number,
                "custom_attached_to_section": custom_attached_to_section,
                "file_name": filename,
                "content": content,
                "custom_type_of_document": custom_type_of_document,
                "is_private": cint(is_private),
                "custom_title_of_document": custom_title_of_document,
                "custom_date": custom_date,
            }
        )
        file_doc.save(ignore_permissions=ignore_permissions)
        uploaded_files.append(file_doc.as_dict())
    owner_user = frappe.db.get_value(doctype, docname, "owner")
    doc = frappe.new_doc("Notification Log")
    doc.for_user = owner_user
    doc.type = "Mention"
    doc.subject = f"{owner_user} attached {custom_type_of_document} to Project Concept-I {docname}"
    doc.document_type = doctype
    doc.document_name = docname

    doc.save()
    frappe.db.commit()
    return uploaded_files
