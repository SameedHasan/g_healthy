import frappe


@frappe.whitelist()
def sign_up():
    """Sign up a new mother/patient and create first pregnancy record"""
    data = frappe.local.request.json
    if frappe.db.exists("User", data["email"]):
        frappe.throw("User already exists")
    user = frappe.get_doc(
        {
            "doctype": "User",
            "email": data["email"],
            "first_name": data["full_name"].split(" ")[0],
            "last_name": " ".join(data["full_name"].split(" ")[1:]),
            "new_password": data["password"],
            "role_profile_name": "Patient",
            "send_welcome_email": 0,
        }
    )
    user.insert()

    if frappe.db.exists("Patient", data["email"]):
        frappe.throw("Patient already exists")

    patient = frappe.get_doc(
        {
            "doctype": "Patient",
            "user_id": user.name,
            **data,
        }
    )
    patient.insert()

    pregnancy = frappe.get_doc(
        {
            "doctype": "Pregnancy",
            "patient": patient.name,
            "status": "Ongoing",
            **data,
        }
    )
    pregnancy.insert()
    return patient
