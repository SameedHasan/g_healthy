import re

import frappe
from frappe.utils.pdf import get_pdf

from g_healthy.apis.query_report import provide_binary_file

from g_healthy.apis.email import get_html_and_style
from datetime import datetime
from calendar import monthrange
from collections import defaultdict


@frappe.whitelist()
def preview_and_download(dt, dn):
    """
    This function generates a PDF preview and returns the PDF content and filename
    for a given document type and name.

    Parameters:
        dt (str): The document type.
        dn (str): The document name.

    Returns:
        tuple: A tuple containing the filename and PDF content.
    """
    pdf_format = (
        frappe.db.get_value("Print Format", {"doc_type": dt, "disabled": 0}, "name")
        or "Standard"
    )

    add_to_doc = {}

    html = frappe.get_print(dt, dn, print_format=pdf_format)

    html = re.sub(
        r'<div class="action-banner print-hide">.*?</div>', "", html, flags=re.DOTALL
    )
    pdf_content = get_pdf(html)

    provide_binary_file(dt, dn, "pdf", pdf_content)
