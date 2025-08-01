import frappe
from frappe.model.base_document import get_controller
from frappe.model.utils import is_virtual_doctype
from frappe.utils import cint
from frappe.utils.data import sbool
from frappe.desk.form.load import get_attachments

from frappe.desk.reportview import (
    get_form_params,
    execute,
)

DISALLOWED_PARAMS = (
    "cmd",
    "data",
    "ignore_permissions",
    "view",
    "user",
    "csrf_token",
    "join",
)


def custom_copy_attachments_from_amended_from(self):

    attachments = get_attachments(self.doctype, self.amended_from) or []

    for attach_item in attachments:
        file_doc = frappe.get_doc("File", attach_item.name)
        file_data = file_doc.as_dict()
        file_data.update(
            {
                "attached_to_name": self.name,
                "attached_to_doctype": self.doctype,
            }
        )
        file_data.pop("name", None)

        _file = frappe.get_doc({"doctype": "File", **file_data})
        _file.save()


@frappe.whitelist()
@frappe.read_only()
def custom_get_count() -> int:

    args = get_form_params()
    if args.get("page_length"):
        args.pop("page_length")
    if args.get("book_versions"):
        args.pop("book_versions")

    if is_virtual_doctype(args.doctype):
        controller = get_controller(args.doctype)
        count = controller.get_count(args)
    else:
        args.distinct = sbool(args.distinct)
        distinct = "distinct " if args.distinct else ""
        args.limit = cint(args.limit)
        fieldname = f"{distinct}`tab{args.doctype}`.name"
        args.order_by = None

        if args.limit:
            args.fields = [fieldname]
            partial_query = execute(**args, run=0)
            count = frappe.db.sql(f"""select count(*) from ( {partial_query} ) p""")[0][
                0
            ]
        else:
            args.fields = [f"count({fieldname}) as total_count"]
            count = execute(**args)[0].get("total_count")

    return count


def handle_session_stopped():
    """Show a custom update message page styled like the React frontend."""
    from frappe.website.serve import get_response

    html = frappe.render_template(
        "g_healthy/templates/pages/custom_update_message.html", {}
    )
    frappe.respond_as_web_page(
        title="System Updating",
        html=html,
        http_status_code=503,
        indicator_color="orange",
        fullpage=True,
        primary_action=None,
    )
    return get_response("message", http_status_code=503)
