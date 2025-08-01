import json
import datetime
from collections import defaultdict
import re

import frappe

from g_healthy.utils import get_request_form_data


@frappe.whitelist()
def get_list(
    doctype,
    start=0,
    page_length=99999999999,
    filters=None,
    order_by="creation desc",
    or_filters=None,
    book_versions=None,
    group_by=None,
    history=0,
):
    roles = frappe.get_roles(frappe.session.user)
    keys = []
    link_keys = []
    try:
        # Parse filters once
        if filters:
            if isinstance(filters, str):
                filters = json.loads(filters)
            if (
                "name" in filters
                and isinstance(filters["name"], list)
                and filters["name"][0].lower() == "in"
            ):
                filters["name"] = ["in", filters["name"][1]]
        else:
            filters = {}
        if book_versions and doctype == "Annual Dev Programme":
            adps = frappe.db.get_all(
                "List of ADPs",
                filters={"parent": book_versions},
                fields=["adp_form"],
            )
            filters["name"] = ["in", [adp.adp_form for adp in adps]]
        # Get metadata and permissions in a single query
        meta = frappe.get_meta(doctype)
        permissions_r = None
        fields = None
        has_multistep_form = 0
        multistep_form_name = ""
        has_tabs, show_non_standard_fields = 0, 0
        is_status = 0
        states = []

        # Cache metadata
        if not hasattr(frappe.local, "_meta_cache"):
            frappe.local._meta_cache = {}

        if doctype not in frappe.local._meta_cache:
            docs = get_meta_bundle(doctype)
            frappe.local._meta_cache[doctype] = docs
        else:
            docs = frappe.local._meta_cache[doctype]

        if docs and docs[0]:
            has_tabs = docs[0].has_tabs
            show_non_standard_fields = docs[0].show_non_standard_fields
            if docs[0].states:
                states = docs[0].states
            if docs[0].has_multistep_form == 1 and docs[0].has_multistep_form:
                has_multistep_form = 1
                multistep_form_name = docs[0].multistep_form_name
            fields = docs[0].fields
            permissions = docs[0].permissions
            if permissions:
                for permission in permissions:
                    if permission.permlevel == 0:
                        if "Administrator" in roles:
                            permissions_r = {
                                "read": 1,
                                "create": 1,
                                "delete": 1,
                                "update": 1,
                                "only_owner": 0,
                            }
                        else:
                            if permission.role in roles:
                                permissions_r = {
                                    "read": permission.read,
                                    "create": permission.create,
                                    "delete": permission.delete,
                                    "update": permission.write,
                                    "only_owner": permission.if_owner,
                                }

        track_seen = meta.track_seen

        # Handle global search efficiently
        global_value = None
        if filters and "global" in filters:
            global_value = filters.pop("global")

        # Get data in a single query with all needed fields
        fields_to_fetch = ["*"]
        if track_seen:
            fields_to_fetch.append("_seen")
        if show_non_standard_fields:
            fields_to_fetch.extend(["owner", "creation", "_assign"])

        re_data = frappe.get_list(
            doctype,
            filters=filters,
            or_filters=or_filters,
            fields=fields_to_fetch,
            order_by=order_by,
            limit_start=start,
            limit_page_length=page_length,
            group_by=group_by,
        )

        # Handle global search filtering
        if global_value:
            filtered_data = []
            for record in re_data:
                for key_dict in keys:
                    field_name = key_dict["key"]
                    if field_name in record and global_value in str(record[field_name]):
                        filtered_data.append(record)
                        break
            re_data = filtered_data
        if book_versions and doctype == "Annual Dev Programme":
            total_count = frappe.db.count(
                "List of ADPs", filters={"parent": book_versions}
            )
        else:
            total_count = frappe.desk.reportview.get_count(
                doctype=doctype, filters=filters
            )

        # Handle link fields efficiently
        if link_keys and re_data:
            # Collect all link field values
            link_values = {}
            for key in link_keys:
                docs_temp = get_meta_bundle(key.options)
                title_field = "name"
                if docs_temp and docs_temp[0] and docs_temp[0].title_field:
                    title_field = docs_temp[0].title_field
                if title_field == "name":
                    continue

                # Collect all unique values
                unique_values = set()
                for dat in re_data:
                    current_key_id = getattr(dat, key.fieldname)
                    if current_key_id:
                        unique_values.add(current_key_id)

                if unique_values:
                    # Fetch all linked documents in one query
                    linked_docs = frappe.get_all(
                        key.options,
                        filters={"name": ["in", list(unique_values)]},
                        fields=["name", title_field],
                    )
                    link_values[key.fieldname] = {
                        doc.name: doc[title_field] for doc in linked_docs
                    }

            # Update records with link values
            for dat in re_data:
                for key in link_keys:
                    if key.fieldname in link_values:
                        current_key_id = getattr(dat, key.fieldname)
                        if current_key_id in link_values[key.fieldname]:
                            setattr(
                                dat,
                                key.fieldname,
                                link_values[key.fieldname][current_key_id],
                            )

        # Handle assignments efficiently
        if re_data and show_non_standard_fields:
            doc_owners = set(dat.owner for dat in re_data if dat.owner)
            owner_names = {}

            if doc_owners:
                user_records = frappe.get_all(
                    "User",
                    filters={"name": ["in", list(doc_owners)]},
                    fields=["name", "full_name"],
                )
                owner_names = {
                    "Administrator": "Admin",
                    **{u.name: u.full_name for u in user_records},
                }

            for dat in re_data:
                dat["owner_name"] = owner_names.get(dat.owner, dat.owner)
            doc_names = [dat.name for dat in re_data]
            if doc_names:
                # Get all assignments in one query
                assign_data = frappe.get_all(
                    doctype,
                    filters={"name": ["in", doc_names]},
                    fields=["name", "_assign"],
                )

                # Get all assigned users in one query
                assigned_users = set()
                for row in assign_data:
                    if row["_assign"]:
                        assigned_users.update(json.loads(row["_assign"]))

                if assigned_users:
                    user_details = frappe.get_all(
                        "User",
                        filters={"email": ["in", list(assigned_users)]},
                        fields=["email", "full_name"],
                    )
                    user_dict = {user.email: user.full_name for user in user_details}

                    # Create assignment dictionary
                    assign_dict = {}
                    for row in assign_data:
                        if row["_assign"]:
                            assigned_users = json.loads(row["_assign"])
                            assign_dict[row["name"]] = [
                                {"email": email, "full_name": user_dict.get(email, "")}
                                for email in assigned_users
                            ]

                    # Update records with assignment data
                    for dat in re_data:
                        dat["owner_name"] = (
                            "Admin"
                            if dat.owner == "Administrator"
                            else frappe.db.get_value("User", dat.owner, "full_name")
                        )
                        if dat.name in assign_dict:
                            dat["_assign"] = assign_dict[dat.name]

        return {
            "values": re_data,
            "total": total_count,
            "states": states,
            "permissions": permissions_r,
            "has_multistep_form": has_multistep_form,
            "multistep_form_name": multistep_form_name,
            "has_tabs": has_tabs,
        }
    except frappe.DoesNotExistError:
        frappe.clear_messages()


def get_meta_bundle(doctype):
    bundle = [frappe.desk.form.meta.get_meta(doctype)]
    for df in bundle[0].fields:
        if df.fieldtype in frappe.model.table_fields:
            bundle.append(
                frappe.desk.form.meta.get_meta(
                    df.options, not frappe.conf.developer_mode
                )
            )
    return bundle


@frappe.whitelist()
def get_filters():
    data = get_request_form_data()
    if not data.get("doctype"):
        return {"keys": []}

    doctype = data.get("doctype")
    planner = data.get("planner")
    keys = []

    try:
        docs = get_meta_bundle(doctype)
        fields = docs[0].fields if docs and docs[0] else []
        if frappe.db.exists("List View Settings", doctype):
            list_view_settings = frappe.get_cached_doc("List View Settings", doctype)
            if list_view_settings.fields:
                list_view_fields = json.loads(list_view_settings.fields)
                for label in list_view_fields:
                    field_metadata = next(
                        (
                            field
                            for field in fields
                            if field.fieldname == label["fieldname"]
                        ),
                        None,
                    )

                    if field_metadata:
                        return_data = (
                            field_metadata.options.split("\n")
                            if field_metadata.fieldtype == "Select"
                            and field_metadata.options
                            else []
                        )
                        link_filter_name = (
                            field_metadata.link_filter_name
                            if field_metadata.fieldtype == "Link"
                            else None
                        )
                        link_filter_value = (
                            field_metadata.link_filter_value
                            if field_metadata.fieldtype == "Link"
                            else None
                        )
                        if (
                            link_filter_name
                            and link_filter_value
                            and "status" in link_filter_name
                        ):
                            link_filter_name, link_filter_value = (
                                remove_keyword_and_value(
                                    link_filter_name, link_filter_value, "status"
                                )
                            )
                        keys.append(
                            {
                                "label": label["label"],
                                "fieldname": field_metadata.fieldname,
                                "key": field_metadata.fieldname,
                                "fieldtype": field_metadata.fieldtype,
                                "show_color": 1 if field_metadata.bold else 0,
                                "field_data": return_data,
                                "options": field_metadata.options,
                                "filter_name": link_filter_name,
                                "filter_value": link_filter_value,
                            }
                        )
                    else:
                        if label["fieldname"] == "name":
                            keys.append(
                                {
                                    "label": label["label"],
                                    "fieldname": "name",
                                    "key": "name",
                                    "fieldtype": "Data",
                                    "show_color": 0,
                                    "field_data": [],
                                    "options": None,
                                    # "filter_name": [],
                                    # "filter_value": [],
                                }
                            )
                if planner:
                    keys.append(
                        {
                            "label": "Region",
                            "fieldname": "region",
                            "key": "region",
                            "fieldtype": "Data",
                            "show_color": 0,
                            "field_data": [],
                            "options": None,
                        }
                    )
                    keys.append(
                        {
                            "label": "Coordinator",
                            "fieldname": "coordinator",
                            "key": "coordinator",
                            "fieldtype": "Data",
                            "show_color": 0,
                            "field_data": [],
                            "options": None,
                        }
                    )
                return {"keys": keys}
        return {
            "keys": [
                {
                    "label": "ID",
                    "fieldname": "name",
                    "key": "name",
                    "fieldtype": "Data",
                    "show_color": 0,
                    "field_data": [],
                    "options": None,
                }
            ]
        }
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        return {"keys": []}


def remove_keyword_and_value(first: str, second: str, keyword: str):
    first_list = [item.strip() for item in first.split(",") if item.strip()]
    second_list = [item.strip() for item in re.findall(r"\[.*?\]", second)]

    if keyword in first_list and len(second_list) > first_list.index(keyword):
        index = first_list.index(keyword)
        first_list.pop(index)
        second_list.pop(index)

    return ", ".join(first_list), ", ".join(second_list)


@frappe.whitelist()
def get_docakge_filter_data():
    jobs = frappe.get_list("Jobs", fields=["name", "job_name"])
    billing_customers = frappe.get_list(
        "Organizations", fields=["name", "company_name"], filters={"type": "Customer"}
    )
    billing_companies = frappe.get_list(
        "Billing Companies", fields=["name", "company_name"]
    )
    return {
        "jobs": jobs,
        "billing_customers": billing_customers,
        "billing_companies": billing_companies,
    }


@frappe.whitelist()
def get_logs_list():
    data = get_request_form_data()
    if isinstance(data.get("filters"), str):
        filters = json.loads(data.get("filters"))
    else:
        filters = data.get("filters")

    order_by = data.get("order_by")
    log_list = {}
    logs = frappe.get_list(
        "Logs",
        fields=["name", "date", "shift", "bucket_used", "jobs"],
        filters={"jobs": filters.get("jobs", "")},
        order_by=order_by,
    )
    if (
        filters.get("general_cargo_group")
        and filters.get("general_cargo_group") == "Overtime"
    ):
        logs_list = get_overtime_logs(logs, filters)
        return logs_list

    else:
        keys = [
            {
                "title": "Event",
                "dataIndex": "event",
                "key": "event",
                "fieldtype": "Data",
                "show_color": 0,
                "field_data": [],
            },
            {
                "title": "Code",
                "dataIndex": "code_group",
                "key": "code_group",
                "fieldtype": "Data",
                "show_color": 0,
                "field_data": [],
            },
            {
                "title": "Date",
                "dataIndex": "date",
                "key": "date",
                "fieldtype": "Date",
                "show_color": 0,
                "field_data": [],
            },
            {
                "title": "Shift",
                "dataIndex": "shift",
                "key": "shift",
                "fieldtype": "Data",
                "show_color": 0,
                "field_data": [],
            },
            {
                "title": "Bucket Used",
                "dataIndex": "bucket_used",
                "key": "bucket_used",
                "fieldtype": "Date",
                "show_color": 0,
                "field_data": [],
            },
            {
                "title": "Start Time",
                "dataIndex": "start_time",
                "key": "start_time",
                "fieldtype": "Time",
                "show_color": 0,
                "field_data": [],
            },
            {
                "title": "End Time",
                "dataIndex": "end_time",
                "key": "end_time",
                "fieldtype": "Time",
                "show_color": 0,
                "field_data": [],
            },
        ]
        log_list["keys"] = keys
        re_data = []
        filters.pop("jobs")
        total = 0
        if logs:
            for log in logs:
                filters["logs"] = log.name
                log_details = frappe.get_list(
                    "Log Details", fields=["*"], filters=filters, order_by=order_by
                )
                for log_detail in log_details:
                    total += 1
                    re_data.append(
                        {
                            "name": log_detail.name,
                            "date": log.date,
                            "shift": log.shift,
                            "bucket_used": log.bucket_used,
                            "code_group": log_detail.code_description,
                            "event": frappe.db.get_value(
                                "Code", log_detail["event"], "code_description"
                            )
                            or "",
                            "start_time": log_detail.start_time,
                            "end_time": log_detail.end_time,
                            "bill_to": log_detail.bill_to,
                            "is_billable": log_detail.is_billable,
                            "general_cargo_group": log_detail.general_cargo_group,
                        }
                    )
        log_list["values"] = re_data
        log_list["total"] = total
        return log_list


def get_overtime_logs(logs, filters):

    log_list = {}
    keys = [
        {
            "title": "Date",
            "dataIndex": "date",
            "key": "date",
            "fieldtype": "Date",
            "show_color": 0,
            "field_data": [],
        },
        {
            "title": "Duration(Hrs)",
            "dataIndex": "elapsed_time",
            "key": "elapsed_time",
            "fieldtype": "Time",
            "show_color": 0,
            "field_data": [],
        },
    ]
    log_list["keys"] = keys
    re_data = []
    filters.pop("jobs")
    total = 0
    logs_by_date = defaultdict(list)

    if logs:
        for log in logs:
            filters["logs"] = log.name
            log_details = frappe.get_list("Log Details", fields=["*"], filters=filters)
            for log_detail in log_details:
                logs_by_date[str(log.date)].append(
                    {
                        "name": log_detail.name,
                        "date": log.get("date"),
                        "start_time": log_detail.start_time,
                        "end_time": log_detail.end_time,
                        "bill_to": log_detail.get("bill_to"),
                        "is_billable": log_detail.is_billable,
                        "general_cargo_group": log_detail.general_cargo_group,
                    }
                )
    for date, log_details in logs_by_date.items():
        total += len(log_details)
        elapsed_time = datetime.timedelta()
        bill_to = ""
        for log_detail in log_details:

            if log_detail["start_time"] and log_detail["end_time"]:
                # Check if start_time and end_time are timedelta, convert them to time
                if isinstance(log_detail["start_time"], datetime.timedelta):
                    start_time = (
                        datetime.datetime.min + log_detail["start_time"]
                    ).time()
                else:
                    start_time = log_detail["start_time"]

                if isinstance(log_detail["end_time"], datetime.timedelta):
                    end_time = (datetime.datetime.min + log_detail["end_time"]).time()
                else:
                    end_time = log_detail["end_time"]

                start_dt = datetime.datetime.combine(datetime.date.min, start_time)
                end_dt = datetime.datetime.combine(datetime.date.min, end_time)
                elapsed_time += end_dt - start_dt
            if not bill_to:
                bill_to = log_detail.get("bill_to", "")

        re_data.append(
            {
                "date": date,
                "bill_to": bill_to,
                "logs": log_details,
                "elapsed_time": str(elapsed_time),
            }
        )

    log_list["values"] = re_data
    log_list["total"] = total
    return log_list


@frappe.whitelist()
def fetch_user_list_settings(ref_doctype, user=None):
    """
    Fetch the list of fields for a given doctype and user.

    Args:
        ref_doctype (str): The doctype to fetch fields for.
        user (str, optional): The user to fetch fields for. Defaults to the current user.

    Returns:
        dict: A dictionary containing the list of fields, selected fields, and the doctype.
    """
    user = user or frappe.session.user

    meta = frappe.get_meta(ref_doctype)

    all_fields = [
        {
            "fieldname": df.fieldname,
            "label": df.label,
            "fieldtype": df.fieldtype,
            "hidden": df.hidden,
            "hidden_from_front": df.hidden_from_front,
        }
        for df in meta.fields
        if not df.hidden
    ]

    # Retrieve user-specific settings
    user_settings = frappe.db.get_value(
        "User List Settings", {"user": user, "ref_doctype": ref_doctype}, "*"
    )

    selected_fields = (
        frappe.parse_json(user_settings.get("fields")) if user_settings else []
    )

    for field in all_fields:
        field["selected"] = field["fieldname"] in selected_fields

    response_fields = [
        {
            "title": field["label"],
            "fieldtype": field["fieldtype"],
            "hidden": field["hidden"],
            "hidden_from_front": field["hidden_from_front"],
            "selected": field["selected"],
            "fieldname": field["fieldname"],
        }
        for field in all_fields
    ]

    selected_fields_response = [field for field in response_fields if field["selected"]]

    return {
        "doctype": ref_doctype,
        "fields": response_fields,
        "keys": selected_fields_response or None,
        "values": selected_fields or None,
        "settings_id": user_settings.get("name") if user_settings else None,
    }
