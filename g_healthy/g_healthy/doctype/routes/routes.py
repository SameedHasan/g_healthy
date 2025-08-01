# Copyright (c) 2023, Sameed Hasan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class Routes(Document):
    def validate(self):
        self.path = self.path.lower()
        if not validate_route(self.path):
            frappe.throw(
                "Path must start with / and has no space or other special characters."
            )


def validate_route(text):
    # Check if the text starts with '/'
    if not text.startswith("/"):
        return False

    # Allow multiple segments (e.g., /foo-bar, /foo/bar, /foo_bar, /foo123)
    # React-style: allow a-z, A-Z, 0-9, -, _, /, and optionally : for params
    if not re.match(r"^/[a-zA-Z0-9_\-/:]*$", text):
        return False

    return True
