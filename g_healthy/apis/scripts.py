from datetime import datetime, timedelta

import frappe


@frappe.whitelist()
def update_doc(doctype):
    """Update documents with the given doctype."""
    doc = frappe.get_all(doctype, fields=["name", "modified"])
    # five_hours_ago = datetime.now() - timedelta(hours=5)
    for d in doc:
        # if d.modified > five_hours_ago:
        #     continue
        document = frappe.get_doc(doctype, d.name)
        document.name = document.name.replace(" ", " ")
        document.save()
        frappe.db.commit()
