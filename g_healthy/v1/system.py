import frappe
import json


@frappe.whitelist()
def get_table_columns(doctype: str) -> list[dict]:
    """Get the columns for a given doctype from list view settings and metadata"""

    # Get list view settings for the doctype
    list_view_settings = frappe.get_doc("List View Settings", doctype)
    columns = []

    # Get metadata for the doctype
    if not list_view_settings:
        return [
            {
                "title": "ID",
                "dataIndex": "name",
                "key": "name",
                "fieldtype": "Data",
                "show_color": 0,
                "is_status": 0,
                "field_data": [],
            }
        ]
    meta = frappe.get_meta(doctype)
    fields = json.loads(list_view_settings.get("fields"))
    # Process each fieldname in list view settings
    for field in fields:
        if not field.get("fieldname"):
            continue
        field_name = field.get("fieldname")
        field_meta = meta.get_field(field_name)
        if field_meta:
            column = {
                "title": field_meta.label or field_name,
                "dataIndex": field_name,
                "key": field_name,
                "fieldtype": field_meta.fieldtype,
                "show_color": 0,
                "is_status": getattr(field_meta, "is_status", 0),
                "field_data": [],
            }
            if field_meta.fieldtype == "Link" and field_meta.options:
                column["field_data"] = [field_meta.options]
            elif field_meta.fieldtype == "Select" and field_meta.options:
                options = [
                    opt.strip() for opt in field_meta.options.split("\n") if opt.strip()
                ]
                column["field_data"] = options
            elif field_meta.fieldtype == "Status":
                column["is_status"] = 1
            columns.append(column)

    return columns
