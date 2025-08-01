from datetime import datetime

import frappe
from frappe import _


def run_after_install():
    create_fiscal_year()
    create_root_accounts()


def after_install():

    doc_type = "DocField"

    # Add field to the DocType
    fields = [
        {
            "depends_on": "",
            "description": "Show this field in parent list view",
            "fieldname": "show_child_in_list",
            "fieldtype": "Check",
            "label": "Show Child In List View",
            "insert_after": "in_list_view",
            "parent": "DocType",
            "mandatory_depends_on": "",
            "doctype": "DocField",
            "parentfield": "fields",
            "parenttype": "DocType",
        }
    ]

    for xfield in fields:
        field = frappe.new_doc("DocField")
        field.label = xfield["label"]
        field.fieldname = xfield["fieldname"]
        field.fieldtype = xfield["fieldtype"]
        field.options = xfield.get("options", "")
        field.description = xfield["description"]
        field.depends_on = xfield["depends_on"]
        field.mandatory_depends_on = xfield["mandatory_depends_on"]
        field.insert_after = xfield["insert_after"]
        field.parent = doc_type
        field.parentfield = xfield["parentfield"]
        field.parenttype = xfield["parenttype"]
        field.insert(ignore_permissions=True)
    frappe.clear_cache(doctype=doc_type)


def create_fiscal_year():
    if not frappe.get_all("Fiscal Year"):

        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month < 7:
            start_year = current_year - 1
        else:
            start_year = current_year

        end_year = start_year + 1
        fiscal_year_name = f"{start_year}-{str(end_year)[-2:]}"

        fiscal_year = frappe.get_doc(
            {
                "doctype": "Fiscal Year",
                "year": fiscal_year_name,
                "from_date": f"{start_year}-07-01",
                "to_date": f"{end_year}-06-30",
                "default_year": 1,
            }
        )
        fiscal_year.insert(ignore_permissions=True)
        frappe.db.commit()


def create_root_accounts():
    root_accounts = [
        {
            "account_name": "Expenditures",
            "root_type": "Expense",
            "account_number": "A",
        },
        {
            "account_name": "Tax Revenue",
            "root_type": "Income",
            "account_number": "B",
        },
        {
            "account_name": "Non-Tax Revenue",
            "root_type": "Income",
            "account_number": "C",
        },
        {
            "account_name": "Capital Receipts",
            "root_type": "Income",
            "account_number": "E",
        },
        {"account_name": "Assets", "root_type": "Asset", "account_number": "F"},
        {
            "account_name": "Liabilities",
            "root_type": "Liability",
            "account_number": "G",
        },
        {
            "account_name": "Equities",
            "root_type": "Equity",
            "account_number": "H",
        },
    ]

    for acc in root_accounts:
        if not frappe.db.exists("Account", {"account_name": acc["account_name"]}):
            account = frappe.get_doc(
                {
                    "doctype": "Account",
                    "account_name": acc["account_name"],
                    "is_group": 1,
                    "root_type": acc["root_type"],
                    "account_number": acc["account_number"],
                    "report_type": (
                        "Balance Sheet"
                        if acc["root_type"] in ["Asset", "Liability", "Equity"]
                        else "Profit and Loss"
                    ),
                }
            )
            account.insert(ignore_permissions=True, ignore_mandatory=True)
            frappe.db.commit()
