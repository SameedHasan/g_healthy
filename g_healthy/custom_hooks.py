import platform

import frappe
import geocoder
import requests


# def validate_on_update(data, method):
#     if frappe.flags.in_migrate:
#         return
#     if data.doctype in [
#         "DefaultValue",
#         "DocShare",
#         "User",
#         "DocType",
#         "Menu Items",
#         "G Healthy",
#         "Version",
#         "Notification Settings",
#         "Comment",
#         "Page",
#         "Report",
#         "Logs Group",
#         "Job Type",
#     ]:
#         return
#     bundle = [frappe.desk.form.meta.get_meta(data.doctype)]
#     for df in bundle[0].fields:
#         if df.fieldtype == "Data" and df.options == "Phone":
#             pass
#         if df.fieldtype in frappe.model.table_fields:
#             bundle.append(
#                 frappe.desk.form.meta.get_meta(
#                     df.options, not frappe.conf.developer_mode
#                 )
#             )
#     doc = bundle[0]

#     if doc and doc.fields:
#         for field in doc.fields:
#             # Implement expression_field logic here
#             if field.expression_field:
#                 try:
#                     expression_field = field.expression_field
#                     result = re.sub(
#                         r"\{([^}]+)\}",
#                         lambda match: replace_keys(match, data),
#                         expression_field,
#                     )
#                     setattr(data, field.fieldname, result)
#                 except:
#                     pass
#             if field.fetch_from_field:
#                 try:
#                     fetch_from_field = field.fetch_from_field
#                     fetch_from_field_data = getattr(data, fetch_from_field)
#                     setattr(data, field.fieldname, fetch_from_field_data)
#                 except:
#                     pass
#             if field.default:
#                 for new_doc in doc.fields:
#                     if (
#                         new_doc.fieldtype == "Table" or new_doc.fieldtype == "Link"
#                     ) and new_doc.options == field.default:
#                         if new_doc.fieldtype == "Table":
#                             child_data = getattr(data, new_doc.fieldname)
#                         elif new_doc.fieldtype == "Link":
#                             link_name = getattr(data, new_doc.fieldname)
#                             if frappe.db.exists(new_doc.options, link_name):
#                                 child_data = frappe.get_doc(new_doc.options, link_name)
#                             else:
#                                 child_data = []
#                         else:
#                             child_data = []
#                         child_bundle = [frappe.desk.form.meta.get_meta(field.default)]
#                         for df in child_bundle[0].fields:
#                             if df.fieldtype in frappe.model.table_fields:
#                                 child_bundle.append(
#                                     frappe.desk.form.meta.get_meta(
#                                         df.options, not frappe.conf.developer_mode
#                                     )
#                                 )
#                         # Fields that needs to be shown in listview
#                         fields_to_add = []
#                         default_value = ""
#                         if child_bundle:
#                             child_doc = child_bundle[0]
#                             if child_doc and child_doc.fields:
#                                 for child_field in child_doc.fields:
#                                     if (
#                                         child_field.in_list_view == 1
#                                         and child_field.fieldtype != "Link"
#                                     ):
#                                         fields_to_add.append(child_field.fieldname)
#                         child_return_data = []
#                         if child_data:
#                             try:
#                                 for child_row in child_data:
#                                     result_values = [
#                                         getattr(child_row, key)
#                                         for key in fields_to_add
#                                         if hasattr(child_row, key)
#                                     ]
#                                     filtered_values = [
#                                         str(value)
#                                         for value in result_values
#                                         if value is not None
#                                     ]
#                                     result_values = ", ".join(map(str, filtered_values))
#                                     child_return_data.append(result_values)
#                                     if len(child_data) == 1:
#                                         default_value = result_values
#                                         setattr(
#                                             data,
#                                             field.fieldname,
#                                             json.dumps(
#                                                 {
#                                                     "default": default_value,
#                                                     "data": [],
#                                                     "single": "no",
#                                                 }
#                                             ),
#                                         )
#                                     else:
#                                         default_value = (
#                                             str(len(child_data)) + " " + field.label
#                                         )
#                                         setattr(
#                                             data,
#                                             field.fieldname,
#                                             json.dumps(
#                                                 {
#                                                     "default": default_value,
#                                                     "data": child_return_data,
#                                                     "single": "no",
#                                                 }
#                                             ),
#                                         )
#                             except:
#                                 result_values = [
#                                     getattr(child_data, key)
#                                     for key in fields_to_add
#                                     if hasattr(child_data, key)
#                                 ]
#                                 filtered_values = [
#                                     str(value)
#                                     for value in result_values
#                                     if value is not None
#                                 ]
#                                 if filtered_values[1]:
#                                     if len(filtered_values[1]) > 25:
#                                         main_value = (
#                                             filtered_values[1][: 25 - 3] + "..."
#                                         )
#                                     else:
#                                         main_value = filtered_values[1]
#                                 elif filtered_values[0]:
#                                     main_value = filtered_values[0]
#                                 else:
#                                     main_value = filtered_values
#                                 result_values = "<br> ".join(map(str, filtered_values))
#                                 default_value = result_values
#                                 setattr(
#                                     data,
#                                     field.fieldname,
#                                     json.dumps(
#                                         {
#                                             "default": main_value,
#                                             "data": filtered_values,
#                                             "single": "yes",
#                                         }
#                                     ),
#                                 )
#                         else:
#                             setattr(
#                                 data,
#                                 field.fieldname,
#                                 json.dumps(
#                                     {"default": "", "data": [], "single": "yes"}
#                                 ),
#                             )


# def validate_after_update(data, method):
#     if frappe.flags.in_migrate:
#         return
#     if data.doctype in [
#         "DefaultValue",
#         "DocShare",
#         "User",
#         "DocType",
#         "Menu Items",
#         "G Healthy",
#         "Version",
#         "Notification Settings",
#         "Comment",
#         "Page",
#         "Report",
#         "Language",
#         "Customize Form",
#         "Logs Group",
#         "Job Type",
#     ]:
#         return
#     linked_doctypes = get_linked_doctypes(data.doctype)
#     if linked_doctypes:
#         for key, value in linked_doctypes.items():
#             if "fieldname" in value and value["fieldname"][0]:
#                 if "child_doctype" in value:
#                     dy_doctype = value["child_doctype"]
#                 else:
#                     dy_doctype = key
#                 if dy_doctype in ["Customize Form"]:
#                     return
#                 fieldname = value["fieldname"][0]
#                 if frappe.db.exists(dy_doctype, {fieldname: data.name}):
#                     available_docs = frappe.get_all(
#                         dy_doctype, fields=["name"], filters={fieldname: data.name}
#                     )
#                     for available_doc in available_docs:
#                         try:
#                             doc_to_update = frappe.get_doc(
#                                 dy_doctype, available_doc.name
#                             )
#                             if "parent" in doc_to_update and doc_to_update.parent:
#                                 parent_doc_update = frappe.get_doc(
#                                     doc_to_update.parenttype, doc_to_update.parent
#                                 )
#                                 temp_name = parent_doc_update.name
#                                 parent_doc_update.name = "TEMP"
#                                 parent_doc_update.name = temp_name
#                                 parent_doc_update.save()
#                             else:
#                                 temp_name = doc_to_update.name
#                                 doc_to_update.name = "TEMP"
#                                 doc_to_update.name = temp_name
#                                 doc_to_update.save()
#                         except:
#                             pass


def get_location():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        data = response.json()
        ip_address = data.get("ip")
        location = geocoder.ip(ip_address)
        city = location.city
        return city
    except Exception as e:
        return "Unknown"


def get_location_ipinfo():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        city = data.get("city")

        if not city:
            return "Error: Could not retrieve city information from IP"

        return city

    except requests.RequestException as e:
        return "Unknown"
    except Exception as e:
        return "Unknown"


def on_session_creation():
    user = frappe.session.user

    # if "request" in frappe.local and "headers" in frappe.local.request:
    user_agent = frappe.local.request.headers.get("User-Agent")

    if "Chrome" in user_agent:
        browser = "Chrome"
    elif "Firefox" in user_agent:
        browser = "Firefox"
    elif "Safari" in user_agent:
        browser = "Safari"
    elif "Edge" in user_agent:
        browser = "Edge"
    elif "MSIE" in user_agent or "Trident/" in user_agent:
        browser = "Internet Explorer"
    else:
        browser = "Unknown"

    # Now, 'browser' holds the detected browser or is set to None if not found.

    ip_address = None
    # if(frappe.local.request.remote_addr):
    if "request" in frappe.local and "remote_addr" in frappe.local.request:
        ip_address = frappe.local.request.remote_addr

    os_platform = platform.system()

    location = get_location_ipinfo()

    user_details = frappe.get_doc("User", user)

    frappe.get_doc(
        {
            "doctype": "Activity Log",
            "subject": "Associated Session Details",
            "ip_address": ip_address,
            "custom_browser": browser,
            "custom_platform": os_platform,
            "custom_log": "True",
            "custom_location": location,
            "session_id": frappe.session.sid,
            "status": "Success",
        }
    ).insert(ignore_permissions=True)

    frappe.db.commit()


def on_logout():
    user = frappe.session.user
    session_id = frappe.session.sid

    activity_log = frappe.get_all(
        "Activity Log", filters={"session_id": session_id}, limit=1
    )

    if activity_log:
        frappe.db.set_value(
            "Activity Log",
            activity_log[0].name,
            "logout_time",
            frappe.utils.now_datetime(),
        )


def replace_keys(match, values):
    key = match.group(1)
    return values.get(key, key)


def custom_naming(doc, method):
    if frappe.flags.in_migrate:
        return
    doc_meta = frappe.get_meta(doc.doctype)
    if doc_meta and doc_meta.naming_rule == "By script":
        doc.naming_series = None

        series_key = doc.doctype

        current_number = frappe.db.get_value(
            "Series", {"name": series_key}, "current", order_by=None
        )

        if current_number is None:
            # If series does not exist, initialize it with 1
            new_number = 1
            frappe.db.sql(
                """INSERT INTO `tabSeries` (`name`, `current`) 
                   VALUES (%s, %s) 
                   ON CONFLICT (`name`) DO NOTHING""",
                (series_key, new_number),
            )
        else:
            # Increment the existing number
            new_number = int(current_number) + 1
            frappe.db.sql(
                """UPDATE `tabSeries` SET `current` = %s WHERE `name` = %s""",
                (new_number, series_key),
            )
        old_number = new_number
        while frappe.db.exists(doc.doctype, {"name": str(new_number)}):
            new_number += 1
        if frappe.db.exists(doc.doctype, {"name": str(old_number)}):
            frappe.db.sql(
                """UPDATE `tabSeries` SET `current` = %s WHERE `name` = %s""",
                (new_number, series_key),
            )

        doc.name = str(new_number)
