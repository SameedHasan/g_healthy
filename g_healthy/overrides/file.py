import frappe
from frappe import _
from frappe.core.doctype.file.file import File
from frappe.desk.reportview import (
    get_form_params,
)

update_dictionary = {
    "MOM": "has_mom_uploaded",
    "Working Paper": "has_working_paper_uploaded",
    "NOC": "has_noc",
    "Admin Approval": "has_admin_approval",
}


class CustomFile(File):
    def validate(self):
        super().validate()
        args = get_form_params()

        if self.custom_type_of_document and self.is_new():
            for key, value in update_dictionary.items():
                if self.custom_type_of_document == key:
                    doc_to_update = frappe.get_doc(
                        self.attached_to_doctype, self.attached_to_name
                    )
                    if args.get("approval_type"):
                        doc_to_update.approval_type = args.get("approval_type")
                    if args.get("custom_type_of_document") == "NOC" and frappe.get_meta(
                        doc_to_update.doctype
                    ).get_field("authorization_date"):
                        doc_to_update.authorization_date = args.get("date")
                    if args.get(
                        "custom_type_of_document"
                    ) == "Admin Approval" and frappe.get_meta(
                        doc_to_update.doctype
                    ).get_field(
                        "approval_date"
                    ):
                        doc_to_update.approval_date = args.get("date")
                        doc_to_update.commencement_start_date = args.get(
                            "commencement_start_date"
                        )
                        doc_to_update.commencement_end_date = args.get(
                            "commencement_end_date"
                        )

                    if doc_to_update:
                        if doc_to_update.status in [
                            "Finalized",
                            "New",
                        ] and not doc_to_update.get("amended_from"):
                            frappe.throw(
                                f"""Documents can only be uploaded after the 
                                {doc_to_update.doctype} is under review."""
                            )
                        if not doc_to_update.get(
                            "docstatus"
                        ) == 1 and not doc_to_update.get("amended_from"):
                            frappe.throw(
                                "Documents can only be uploaded after the pc1 is finalized."
                            )
                        doc_to_update.update({value: 1})
                        doc_to_update.save()

            frappe.db.commit()
