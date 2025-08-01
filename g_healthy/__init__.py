__version__ = "15.0.0"


def override_document_methods():
    from frappe.desk import reportview
    from frappe.model.document import Document
    from frappe.utils import response

    from g_healthy.overrides.document import (
        custom_copy_attachments_from_amended_from,
        custom_get_count,
        handle_session_stopped,
    )

    Document.copy_attachments_from_amended_from = (
        custom_copy_attachments_from_amended_from
    )
    reportview.get_count = custom_get_count
    response.handle_session_stopped = handle_session_stopped


# Call the override function on app load
override_document_methods()
