import frappe
from frappe import _


@frappe.whitelist()
def process_doctype_changes(doctype, data):
    """
    This function takes a payload containing a doctype and a data object with arrays of
    "addArray", "updateArray" and "deleteArray".
    It processes these arrays and inserts, updates or
    deletes the corresponding documents in the given doctype.\n
    The function returns a dictionary with the keys "inserted", "updated" and "deleted"
    containing the names of the documents that were inserted, updated or deleted.\n
    The function will throw an error if the payload does not contain a doctype or
    if the name of a document is missing in an update or delete payload.\n
    """
    try:
        return_data = {"inserted": [], "updated": [], "deleted": []}

        if not doctype:
            frappe.throw(_("Doctype not specified in payload"))

        # Handle Additions
        add_array = data.get("addArray", [])
        for item in add_array:
            new_doc = frappe.new_doc(doctype)
            new_doc.update(item)
            new_doc.insert(ignore_permissions=True)
            return_data["inserted"].append(new_doc.name)
        # Handle Updates
        update_array = data.get("updateArray", [])
        for item in update_array:
            doc_name = item.get("name")
            if not doc_name:
                frappe.throw(_("Document name missing in update payload"))
            doc = frappe.get_doc(doctype, doc_name)
            doc.update(item)
            doc.save(ignore_permissions=True)
            return_data["updated"].append(doc.name)

        # Handle Deletions
        delete_array = data.get("deleteArray", [])
        for item in delete_array:
            doc_name = item.get("name")
            if not doc_name:
                frappe.throw(_("Document name missing in delete payload"))
            frappe.delete_doc(doctype, doc_name, ignore_permissions=True)
            return_data["deleted"].append(doc_name)

        return return_data

    except Exception as e:
        frappe.log_error(
            frappe.get_traceback(), _("Error in handle_crane_working_times")
        )
        frappe.throw(str(e))
