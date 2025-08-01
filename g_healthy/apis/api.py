import os
import re
from datetime import datetime
import json

import frappe
from frappe import _
import frappe.permissions
from frappe.desk.search import build_for_autosuggest, search_widget
from frappe.model.utils.user_settings import get_user_settings
from frappe.sessions import clear_sessions, delete_session
from frappe.utils.password import update_password

from g_healthy.utils import get_request_form_data
from g_healthy.apis.list import get_list as custom_get_list


@frappe.whitelist()
def get_logged_user():
    doc = frappe.get_doc("User", frappe.session.user)
    user_roles = []
    user_roles = frappe.get_roles(frappe.session.user)
    file_id = None
    if doc.user_image:
        file_id = frappe.get_value("File", {"file_url": doc.user_image}, "name")
    curr_user = {
        "name": doc.name,
        "email": doc.email,
        "full_name": doc.full_name,
        "first_name": doc.first_name,
        "last_name": doc.last_name,
        "username": doc.username,
        "roles": user_roles,
        "image": doc.user_image,
        "file_id": file_id,
        "mobile_no": doc.mobile_no,
        "location": doc.location,
        "last_password_reset": doc.last_password_reset_date,
        "session_id": frappe.session.sid,
        "role_profile_name": doc.role_profile_name,
    }

    return curr_user


@frappe.whitelist()
def check_password():
    post_data = get_request_form_data()
    user = frappe.session.user
    pwd = post_data.get("pwd")

    try:
        if pwd is None:
            raise frappe.ValidationError(_("Password cannot be None"))

        if not frappe.local.login_manager.check_password(user, pwd):
            raise frappe.AuthenticationError(_("Incorrect password"))

        return {"success": True, "message": _("Password is correct")}
    except frappe.AuthenticationError:
        frappe.throw(
            _("Incorrect password"), user=user, title=_("Authentication Failed")
        )
    except frappe.ValidationError as e:
        frappe.throw(str(e))


@frappe.whitelist()
def update_user_password():
    post_data = get_request_form_data()

    user = frappe.session.user
    pwd = post_data.get("new_password")
    user_doc = frappe.get_doc("User", user)

    update_password(user, pwd, logout_all_sessions=True)
    user_doc.last_password_reset_date = frappe.utils.now_datetime()
    user_doc.save()
    frappe.db.commit()

    return user_doc


@frappe.whitelist()
def getdoctype(
    doctype,
    with_parent=False,
    cached_timestamp=None,
    name=None,
    showall=False,
    selectedfieldname=None,
    selectedfieldvalue=None,
    only_send_ticket_type=False,
    event_data=False,
    field_name=None,
):
    """
    Returns doctype fields including their metadata that is used to generate forms on frontend
    method
    ------
    GET

    Params
    ------
    doctype
    with_parent
    cached_timestamp

    Response
    --------
    Object
    """

    docs = []
    parent_dt = None

    try:
        if name and frappe.db.exists(doctype, name):
            doc_data = frappe.get_doc(doctype, name)
        else:
            doc_data = None
    except:
        doc_data = None
    try:
        if not frappe.permissions.has_permission(doctype, "read"):
            frappe.throw(
                _("You don't have permission to read {0}").format(doctype),
                frappe.PermissionError,
            )
        elif name and not frappe.permissions.has_permission(doctype, "read", name):
            frappe.throw(
                _("You don't have permission to read {0}").format(doctype),
                frappe.PermissionError,
            )
    except frappe.PermissionError:
        frappe.throw(
            _("You don't have permission to read {0}").format(doctype),
            frappe.PermissionError,
        )
    docstatus = 0

    if with_parent and (parent_dt := frappe.model.meta.get_parent_dt(doctype)):
        docs = get_meta_bundle(parent_dt)
        frappe.response["parent_dt"] = parent_dt

    if not docs:
        docs = get_meta_bundle(doctype, field_name)

    frappe.response["user_settings"] = get_user_settings(parent_dt or doctype)

    if cached_timestamp and docs[0].modified == cached_timestamp:
        return "use_cache"

    return_obj = []
    if docs:
        i = 0
        formwidth = "700px"
        for doc in docs:
            if name:
                docstatus = frappe.db.get_value(doctype, name, "docstatus")
            if i == 0 and doc.fields:
                for field in doc.fields:
                    if field.print_width == "8":
                        formwidth = "900px"

            properties = get_cleared_fields(
                doc.fields,
                doc_data,
                doc.permissions,
                showall,
                doctype,
                name,
                selectedfieldname,
                selectedfieldvalue,
                only_send_ticket_type=only_send_ticket_type,
                event_data=event_data,
            )

            temp_obj = {
                "doctype": doc.doctype,
                "name": doc.name,
                "docstatus": docstatus,
                "properties": properties,
                "permissions": get_user_permissions(doc.permissions),
                "formwidth": formwidth,
            }
            return_obj.append(temp_obj)
            i += 1

    if name and not frappe.db.exists(doctype, name):
        return_obj.append({"error": "Record not found"})
    return return_obj


def get_meta_bundle(doctype, field_name=None):
    """
    Its a helper function to get meta information of
        a doctype using frappe utils
    """
    bundle = [frappe.desk.form.meta.get_meta(doctype)]
    for df in bundle[0].fields:
        if df.fieldtype in frappe.model.table_fields:
            bundle.append(
                frappe.desk.form.meta.get_meta(
                    df.options, not frappe.conf.developer_mode
                )
            )
        if df.fieldtype == "Section Break" and df.acts_as_child:
            options = (
                df.options.split("\n")
                if df.fieldtype == "Section Break"
                else df.options
            )
            fieldname_options_map = {
                "pc_i_accounts": "One Time Cost Estimation",
                "pci_accounts": "General Recurring Cost Estimates",
            }
            if field_name:
                options = fieldname_options_map.get(field_name, options)
                bundle.append(
                    frappe.desk.form.meta.get_meta(
                        options, not frappe.conf.developer_mode
                    )
                )
            else:
                bundle.append(
                    frappe.desk.form.meta.get_meta(
                        options, not frappe.conf.developer_mode
                    )
                )
    return bundle


def get_cleared_fields(
    fields,
    doc_data,
    permissions,
    showall,
    doctype,
    name,
    selectedfieldname,
    selectedfieldvalue,
    only_send_ticket_type,
    event_data=False,
):
    """
    Give DocFields to this function and it will
        provide only needed meta fields and their values
    """
    return_doc = []
    if fields:
        for field in fields:
            if field.hidden_from_front == 1 and not showall:
                continue
            if selectedfieldname and selectedfieldvalue and field.depends_on:
                check = check_eval_value(
                    field.depends_on, selectedfieldname, selectedfieldvalue
                )
                if not check:
                    continue
            if only_send_ticket_type and field.fieldname != "ticket_type":
                continue
            parsed_depends_on = (
                parse_depends_on(field.depends_on) if field.depends_on else None
            )
            temp_doc = {
                **field.__dict__,
                "hidden": get_hidden_info(field, permissions),
                "reqd": check_req_val(
                    field=field,
                    selectedfieldname=selectedfieldname,
                    selectedfieldvalue=selectedfieldvalue,
                ),
                "filter_name": field.link_filter_name,
                "filter_value": field.link_filter_value,
                "read_only": get_read_info(field, permissions),
                "field_data": get_field_data(field, doctype, name, event_data),
                "default_value": get_default_value(field, doc_data, doctype),
                "depends_on": parsed_depends_on,
                "span": field.print_width,
            }

            return_doc.append(temp_doc)
    return return_doc


def parse_depends_on(depends_on):
    """
    Parses Frappe's `depends_on` string and converts it into a structured JSON object.
    Handles:
    - Logical operators (AND `&&`, OR `||`, NOT `!`)
    - Conditions (`==`, `!=`, `in`, `not in`)
    - Fixes invalid Frappe `in (...)` syntax to JavaScript's `in ["A", "B"]`
    - Removes "doc." prefix
    """
    conditions = []
    depends_on = depends_on.replace("eval:", "").strip()
    depends_on = depends_on.replace(";", "").strip()

    or_conditions = depends_on.split(" || ")

    for or_condition in or_conditions:
        and_conditions = or_condition.split(" && ")
        and_group = {}

        for condition in and_conditions:
            condition = condition.strip()

            # Remove "doc." prefix
            condition = condition.replace("doc.", "", 1)

            # Fix invalid `in (...)` syntax → Convert `in ('A', 'B')` to `in ["A", "B"]`
            condition = re.sub(r"in\s*\(([^)]+)\)", r"in [\1]", condition)

            if "==" in condition:
                key, value = condition.split("==")
                # and_group[key.strip()] = value.strip()
                and_group[key.strip()] = {"==": value.strip()}
            elif "!=" in condition:
                key, value = condition.split("!=")
                and_group[key.strip()] = {"!=": value.strip()}
            elif "not in" in condition:
                key, value = condition.split("not in")
                and_group[key.strip()] = {"not_in": value.strip()}
            elif "in" in condition:
                key, value = condition.split("in")
                and_group[key.strip()] = {"in": value.strip()}
            else:
                and_group[condition.strip()] = True

        conditions.append(and_group)

    return conditions if len(conditions) > 1 else conditions[0]


def check_req_val(field, selectedfieldname, selectedfieldvalue):
    if not field.mandatory_depends_on or (
        not selectedfieldname and not selectedfieldvalue
    ):
        return field.reqd
    else:
        return check_eval_value(
            field.mandatory_depends_on, selectedfieldname, selectedfieldvalue
        )


def check_eval_value(expression, selectedfieldname, selectedfieldvalue):
    """
    This function checks for eval part of depends on and
    equired fields and returns True and False based on the eval expression
    """
    # First, remove 'eval:' and potential semicolon at the end for cleaner processing
    clean_expression = expression.replace("eval:", "").strip().rstrip(";")

    conditions = clean_expression.split("||")

    # Evaluate each condition
    for condition in conditions:
        pattern = r'doc\.(\w+)\s*(==|!=)\s*["\']([^"\']+)["\']'
        match = re.match(pattern, condition.strip())

        if match:
            field_name, operator, field_value = match.groups()

            if field_name == selectedfieldname:
                if operator == "==" and field_value == selectedfieldvalue:
                    return True
                elif operator == "!=" and field_value != selectedfieldvalue:
                    return True
    return False


def get_field_data(field, doctype, name, event_data=False):
    """
    For a particular field this function provides its value that is saved in DB.
    This function is useful when you need a doctype metadata for an Update Form
    """

    if (
        doctype in ["Log Details", "General Cargo Other Items"]
        and field.fieldname == "event"
    ):
        total_data = []
        codeGroup = frappe.get_all(
            "Logs Group", fields=["*"], filters={"status": ["!=", "Active"]}
        )
        # Extract the 'name' fields
        names = [item["name"] for item in codeGroup]
        # Create the required array with "Not Like"
        result = ["not in", names]
        codes = frappe.get_all(
            "Code",
            fields=["*"],
            filters={"status": ["!=", "Inactive"], "code_group": result},
            order_by="log_code_no asc",
        )
        if codes:
            for code in codes:
                total_data.append(
                    {
                        "description": code.code_group,
                        "value": code.name,
                        "label": code.code,
                    }
                )
        return total_data
    # Added code for showing options in event in General Cargo Invoice
    if event_data and field.fieldname == "event":
        total_data = []
        codeGroup = frappe.get_all(
            "Logs Group", fields=["*"], filters={"status": ["!=", "Active"]}
        )
        # Extract the 'name' fields
        names = [item["name"] for item in codeGroup]
        # Create the required array with "Not Like"
        result = ["not in", names]
        codes = frappe.get_all(
            "Code",
            fields=["*"],
            filters={"status": ["!=", "Inactive"], "code_group": result},
            order_by="log_code_no asc",
        )
        if codes:
            for code in codes:
                total_data.append(
                    {
                        "description": code.code_group,
                        "value": code.name,
                        "label": code.code,
                    }
                )
        return total_data
    return []
    if (
        field.fieldtype == "Link" or field.fieldtype == "Table MultiSelect"
    ) and field.options:
        if (
            field.fieldtype == "Link"
            and field.link_filter_name
            and field.link_filter_value
            and doctype == "Barges"
            and field.options == "Barge Loading"
            and name
        ):
            if frappe.__version__.startswith("14"):
                search_widget(
                    txt="",
                    doctype=field.options,
                    filters={
                        field.link_filter_name: field.link_filter_value,
                        "jobs": name,
                    },
                    page_length=99999999999,
                )
                return_data = build_for_autosuggest(
                    frappe.response["values"], doctype=field.options
                )
                del frappe.response["values"]
            else:
                results = search_widget(
                    txt="",
                    doctype=field.options,
                    filters={
                        field.link_filter_name: field.link_filter_value,
                        "jobs": name,
                    },
                    page_length=99999999999,
                )
                return_data = build_for_autosuggest(results, doctype=field.options)
        elif (
            field.fieldtype == "Link"
            and field.link_filter_name
            and field.link_filter_value
        ):
            if frappe.__version__.startswith("14"):
                search_widget(
                    txt="",
                    doctype=field.options,
                    filters={field.link_filter_name: field.link_filter_value},
                    page_length=99999999999,
                )
                return_data = build_for_autosuggest(
                    frappe.response["values"], doctype=field.options
                )
                del frappe.response["values"]
            else:
                results = search_widget(
                    txt="",
                    doctype=field.options,
                    filters={field.link_filter_name: field.link_filter_value},
                    page_length=99999999999,
                )
                return_data = build_for_autosuggest(results, doctype=field.options)
        else:
            if doctype == "Barges" and field.options == "Barge Loading" and name:
                if frappe.__version__.startswith("14"):
                    search_widget(
                        txt="",
                        doctype=field.options,
                        filters={"jobs": name},
                        page_length=99999999999,
                    )
                    return_data = build_for_autosuggest(
                        frappe.response["values"], doctype=field.options
                    )
                    del frappe.response["values"]
                else:
                    results = search_widget(
                        txt="",
                        doctype=field.options,
                        filters={"jobs": name},
                        page_length=99999999999,
                    )
                    return_data = build_for_autosuggest(results, doctype=field.options)
            else:
                if frappe.__version__.startswith("14"):
                    search_widget(
                        txt="", doctype=field.options, page_length=99999999999
                    )
                    return_data = build_for_autosuggest(
                        frappe.response["values"], doctype=field.options
                    )
                    del frappe.response["values"]
                else:
                    results = search_widget(
                        txt="", doctype=field.options, page_length=99999999999
                    )
                    return_data = build_for_autosuggest(results, doctype=field.options)
        if return_data and doctype == "Barges" and name:
            for dd in return_data:
                if (
                    dd["value"]
                    and name
                    and frappe.db.exists(
                        "Barge Loading", {"name": dd["value"], "jobs": name}
                    )
                ):
                    barge_info = frappe.get_doc(
                        "Barge Loading", {"name": dd["value"], "jobs": name}
                    )
                    if barge_info.color:
                        dd["color"] = barge_info.color
                    else:
                        dd["color"] = ""
                    if barge_info.bol:
                        dd["bol"] = barge_info.bol
                    else:
                        dd["bol"] = ""

        return return_data
    else:
        return {}


def get_default_value(field, doc_data, doctype):
    """
    Get default value for a field
    """
    try:
        if not doc_data:
            return None
        # if field.fieldtype == "Table MultiSelect" or field.fieldtype == "Table":
        # 	return None
        # custom logic for log details
        cur_val = doc_data.get(field.fieldname)
        return cur_val
    except:
        return "err"


def get_user_permissions(permissions):
    """
    This function converts frappe permissions object to a simple object with only needed fields
    """
    roles = frappe.get_roles(frappe.session.user)
    if permissions:
        for permission in permissions:
            for role in roles:
                if role in permission.role:
                    if permission.permlevel == 0:
                        if "Administrator" in roles:
                            return {
                                "read": 1,
                                "create": 1,
                                "delete": 1,
                                "update": 1,
                                "only_owner": 0,
                            }
                        else:
                            return {
                                "read": permission.read,
                                "create": permission.create,
                                "delete": permission.delete,
                                "update": permission.write,
                                "only_owner": permission.if_owner,
                            }

    return {
        "read": 0,
        "create": 0,
        "delete": 0,
        "update": 0,
        "only_owner": 0,
    }

    # roles = frappe.get_roles(frappe.session.user)
    # permissions_to_return = []
    # if permissions:
    #     for permission in permissions:
    #         for role in roles:
    #             if role in permission.role:
    #                 permissions_to_return.append(permission)

    # return permissions_to_return


def get_hidden_info(field, permissions):
    """
    Based on user permission this function decides if we need to show or hide a particular field
    """
    roles = frappe.get_roles(frappe.session.user)
    if field.hidden == 1:
        return 1
    else:
        return 0
    # The below code is to handle field level permissions that needs to be improved.
    if "Administrator" in roles:
        return 0
    if permissions:
        for permission in permissions:
            if permission.role in roles:
                if (
                    field.permlevel == 0
                    and permission.permlevel == 0
                    and permission.create == 0
                    and permission.write == 0
                ):
                    return 1
                elif field.permlevel == 0:
                    return 0
                if (
                    field.permlevel == permission.permlevel
                    and permission.read == 1
                    and permission.write == 0
                    and permission.role in roles
                ):
                    return 0
                elif (
                    field.permlevel == permission.permlevel
                    and permission.write == 0
                    and permission.role in roles
                ):
                    return 1
                elif (
                    field.permlevel == permission.permlevel
                    and permission.write == 1
                    and permission.role in roles
                ):
                    return 0
    if field.permlevel == 0:
        return 0
    return 1


def get_read_info(field, permissions):
    """
    based on provided permissions this function decides if to set a field to readonly or not
    """
    roles = frappe.get_roles(frappe.session.user)
    if field.read_only == 1:
        return 1
    else:
        return 0
    # The below code is to handle field level permissions that needs to be improved.
    if "Administrator" in roles:
        return 0
    if permissions:
        for permission in permissions:
            if permission.role in roles:
                if (
                    field.permlevel == 0
                    and permission.permlevel == 0
                    and permission.create == 1
                    and permission.read == 1
                ):
                    return 0
                elif (
                    field.permlevel == 0
                    and permission.permlevel == 0
                    and permission.create == 0
                    and permission.write == 0
                    and permission.read == 1
                ):
                    return 1
                elif (
                    field.permlevel == 0
                    and permission.permlevel == 0
                    and permission.read == 1
                    and permission.write == 1
                ):
                    return 0
                elif (
                    field.permlevel == permission.permlevel
                    and permission.read == 1
                    and permission.write == 0
                    and permission.role in roles
                ):
                    return 1
    return 0


@frappe.whitelist()
def after_install():
    """
    This function is fired on the time of installation of the app. It creates fields into the core doctypes
    """
    # Add field to the DocType
    fields = [
        {
            "doctype": "DocField",
            "name": "k6d3d34fc8",
            "idx": 29,
            "depends_on": "",
            "description": "",
            "fieldname": "home_address",
            "fieldtype": "Data",
            "label": "Home Address",
            "parent": "User",
            "mandatory_depends_on": "",
            "parentfield": "fields",
            "parenttype": "DocType",
            "options": "",
        },
        {
            "doctype": "DocField",
            "name": "k6dldb978l",
            "idx": 29,
            "depends_on": "",
            "description": "",
            "fieldname": "other_address",
            "fieldtype": "Data",
            "label": "Other Address",
            "parent": "User",
            "mandatory_depends_on": "",
            "parentfield": "fields",
            "parenttype": "DocType",
            "options": "",
        },
    ]

    for xfield in fields:
        # Construct the SQL query
        if frappe.db.exists(
            xfield["doctype"],
            {
                "parent": xfield["parent"],
                "parentfield": xfield["parentfield"],
                "fieldname": xfield["fieldname"],
            },
        ):
            continue
        sql_query = """
			INSERT INTO `tabDocField`
			(
				`name`, `idx`, `depends_on`, `description`, `fieldname`, `fieldtype`, `label`,
				`parent`, `mandatory_depends_on`, `parentfield`, `parenttype`, `options`
			)
			VALUES
			(
				%(name)s, %(idx)s, %(depends_on)s, %(description)s, %(fieldname)s, %(fieldtype)s, %(label)s,
				%(parent)s, %(mandatory_depends_on)s, %(parentfield)s, %(parenttype)s, %(options)s
			)
		"""

        # Execute the SQL query with the field values
        # frappe.db.sql(sql_query, values=xfield, as_dict=True)

        # Commit the transaction if needed
        # frappe.db.commit()

    # Clear DocType cache
    frappe.clear_cache(doctype=xfield["parent"])


@frappe.whitelist()
def upload_user_image():
    """
    This is a custom function to add a user's image to the filesystems.
    This function was written as the default file upload function had problems.
    """
    # Access the uploaded file
    uploaded_file = frappe.request.files.get("image")

    if not uploaded_file:
        return _("No file uploaded.")
    user_id = frappe.session.user
    timestamp = frappe.utils.now_datetime().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{user_id}_{timestamp}_{uploaded_file.filename}"
    uploaded_file.filename = unique_filename
    uploaded_file.file_url = f"/public/files/{unique_filename}"
    # Save the file in the File System
    file_doc = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": unique_filename,
            "attached_to_doctype": "User",
            "attached_to_name": frappe.session.user,
            "file_url": f"/public/files/{unique_filename}",
            "content": uploaded_file.read(),
        }
    )

    file_doc = file_doc.save(ignore_permissions=True)
    duplicate_file = frappe.get_value(
        "File",
        {"content_hash": file_doc.content_hash, "is_private": file_doc.is_private},
        ["file_url", "name"],
        as_dict=True,
    )
    if duplicate_file:
        if file_doc.is_private:
            file_doc.file_url = f"/private/files/{unique_filename}"
        else:
            file_doc.file_url = f"/files/{unique_filename}"

        fpath = file_doc.write_file()

    # Update the user's user_image field with the file path
    frappe.db.set_value(
        "User", frappe.session.user, "user_image", f"/files/{unique_filename}"
    )

    return _("File uploaded successfully.")


@frappe.whitelist()
def get_user_details():
    """
    This function combines User and User Details table and return an object
    """
    user = frappe.session.user
    other_details = {}
    if frappe.db.exists("User", user):
        user_details = frappe.get_doc(
            "User",
            user,
        )
        if frappe.db.exists("User Fields", {"user": user}):
            other_details = frappe.get_doc("User Fields", {"user": user}, as_dict=True)
        return {"main_details": user_details, "other_details": other_details}


@frappe.whitelist()
def update_user_details():
    """
    this function takes data from POST api and updates the doctypes User and User Details
    """
    post_data = get_request_form_data()
    user = frappe.session.user
    if frappe.db.exists("User Fields", {"user": user}):
        user_detail = frappe.get_doc("User Fields", {"user": user})
        if "home_street" in post_data:
            user_detail.home_street = post_data.home_street
        if "home_city" in post_data:
            user_detail.home_city = post_data.home_city
        if "home_state" in post_data:
            user_detail.home_state = post_data.home_state
        if "home_country" in post_data:
            user_detail.home_country = post_data.home_country
        if "zip_code" in post_data:
            user_detail.zip_code = post_data.zip_code
        if "other_street" in post_data:
            user_detail.other_street = post_data.other_street
        if "other_city" in post_data:
            user_detail.other_city = post_data.other_city
        if "other_state" in post_data:
            user_detail.other_state = post_data.other_state
        if "other_country" in post_data:
            user_detail.other_country = post_data.other_country
        if "other_zip_code" in post_data:
            user_detail.other_zip_code = post_data.other_zip_code
        user_detail.save()
        frappe.db.commit()
    else:
        frappe.get_doc(
            {
                "doctype": "User Fields",
                "home_street": post_data.home_street,
                "home_city": post_data.home_city,
                "home_state": post_data.home_state,
                "home_country": post_data.home_country,
                "zip_code": post_data.zip_code,
                "other_street": post_data.other_street,
                "other_city": post_data.other_city,
                "other_state": post_data.other_state,
                "other_country": post_data.other_country,
                "other_zip_code": post_data.other_zip_code,
                "user": user,
            }
        ).insert()
        frappe.db.commit()


def write_file(self):
    """write file to disk with a random name (to compare)"""
    if self.is_remote_file:
        return

    file_path = self.get_full_path()

    if isinstance(self._content, str):
        self._content = self._content.encode()

    with open(file_path, "wb+") as f:
        f.write(self._content)
        os.fsync(f.fileno())

    frappe.local.rollback_observers.append(self)

    return file_path


@frappe.whitelist()
def destroy_session():
    try:
        user = frappe.session.user
        request_data = get_request_form_data()
        session_id = request_data.get("session_id")
        delete_session(session_id)
        clear_sessions(user)
        update_logout_time(session_id)
        frappe.db.commit()
        # return("response",response)

        return {"message": "error while logging out"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def update_logout_time(session_id):
    session_doc = frappe.get_doc("Activity Log", {"session_id": session_id})
    session_doc.logout_time = datetime.now()
    session_doc.save(ignore_permissions=True)


@frappe.whitelist()
def check_permissions(doctype=""):
    """
    This function checks if the current user has read, write, delete, and create
    permissions for a given document type.

    Parameters:
        doctype (str): The name of the document type.

    Returns:
        dict: A dictionary containing the read, write, delete, and create permissions
        for the document type.
    """

    if not doctype:
        return

    if frappe.permissions.has_permission(
        doctype=doctype, ptype="read", doc=None, user=frappe.session.user
    ):
        read = 1
    else:
        read = 0
    if frappe.permissions.has_permission(
        doctype=doctype, ptype="write", doc=None, user=frappe.session.user
    ):
        write = 1
    else:
        write = 0
    if frappe.permissions.has_permission(
        doctype=doctype, ptype="delete", doc=None, user=frappe.session.user
    ):
        delete = 1
    else:
        delete = 0
    if frappe.permissions.has_permission(
        doctype=doctype, ptype="create", doc=None, user=frappe.session.user
    ):
        create = 1
    else:
        create = 0
    return {
        "read": read,
        "create": create,
        "delete": delete,
        "update": write,
        "only_owner": 0,
    }


@frappe.whitelist()
def version_history(doctype, filters):
    """
    This function returns the list of all previous versions of a document.

    Parameters:
        doctype (str): The name of the document type.
        docname (str): The name of the document.
    Returns:
        list: A list of all previous versions of a document.
    """
    history = []
    if not filters:
        frappe.throw("Filters required")
    if isinstance(filters, str):
        filters = json.loads(filters)
    current_docname = filters.get("name", "")
    latest_docname = current_docname
    if not current_docname:
        raise FileNotFoundError
    while current_docname:
        history.append(current_docname)
        current_doc = frappe.get_doc(doctype, current_docname)
        current_docname = getattr(current_doc, "amended_from", None)
    if latest_docname in history:
        history.remove(latest_docname)
    return custom_get_list(
        doctype=doctype,
        filters={"name": ["in", history]},
        order_by="creation desc",
        history=1,
    )
