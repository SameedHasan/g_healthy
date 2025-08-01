import json

import frappe
from frappe.utils.pdf import get_pdf
from frappe.www.printview import (
    get_print_format_doc,
    get_print_style,
    get_rendered_template,
    set_link_titles,
)


@frappe.whitelist()
def get_html_and_style(
    doc: str,
    name: str | None = None,
    print_format: str | None = None,
    no_letterhead: bool | None = None,
    letterhead: str | None = None,
    trigger_print: bool = False,
    style: str | None = None,
    settings: str | None = None,
    add_to_doc: dict | None = None,
):
    """Returns `html` and `style` of print format, used in PDF etc"""

    if isinstance(name, str):
        document = frappe.get_doc(doc, name)
    else:
        document = frappe.get_doc(json.loads(doc))

    if add_to_doc:
        document.update(add_to_doc)

    document.check_permission()

    print_format = get_print_format_doc(print_format, meta=document.meta)
    set_link_titles(document)

    try:
        html = get_rendered_template(
            doc=document,
            print_format=print_format,
            meta=document.meta,
            no_letterhead=no_letterhead,
            letterhead=letterhead,
            trigger_print=trigger_print,
            settings=frappe.parse_json(settings),
        )
    except frappe.TemplateNotFoundError:
        frappe.clear_last_message()
        html = None

    return {
        "html": html,
        "style": get_print_style(style=style, print_format=print_format),
    }


def generate_pdf(invoice_number):
    """
    Generate a PDF for a dockage invoice based on the given invoice number.

    This function retrieves the invoice and associated job data, along with
    the customer's company name and transaction logs related to the dockage
    invoice. It then generates an HTML representation of the invoice with
    additional document data and converts it into a PDF.

    Parameters:
    - invoice_number (str): The unique identifier of the dockage invoice.

    Returns:
    - pdf_data (bytes): The PDF content generated for the dockage invoice.
    """

    invoice_data = frappe.get_doc("Dockage", invoice_number)
    jobs = frappe.get_doc("Jobs", invoice_data.job)

    customer = frappe.db.get_value(
        "Organizations", invoice_data.billing_customer, "company_name"
    )
    logs_transactions = frappe.get_all(
        "Dockage Transaction Log",
        filters={"dockage_invoice": invoice_data.name},
        fields=["date_received", "amount_received"],
    )

    add_to_doc = {
        "company_name": customer,
        "job_name": jobs.job_name,
        "vessel_name": jobs.vessel_name,
        "location": jobs.location,
        "transactions": logs_transactions,
    }

    response = get_html_and_style(
        "Dockage",
        invoice_number,
        print_format="Dockage",
        add_to_doc=add_to_doc,
        letterhead="Invoices Letterhead",
    )

    pdf_data = get_pdf(response.get("html"), {"orientation": "Landscape"})
    return pdf_data
