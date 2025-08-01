# Copyright (c) 2025, MicroMerger and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Pregnancy(Document):
    """
    Pregnancy document.
    """

    def before_insert(self):
        """
        Before inserting a new pregnancy.
        Check if the patient already has an active pregnancy.
        If so, throw an error.
        """
        if frappe.db.exists(
            "Pregnancy", {"patient": self.patient, "status": "Ongoing"}
        ):
            frappe.throw("Patient already has an active pregnancy")
