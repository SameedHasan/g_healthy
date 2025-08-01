import json

import frappe
from frappe import _
from frappe.desk.search import build_for_autosuggest, search_widget

from g_healthy.utils import get_request_form_data


@frappe.whitelist()
def save_logs():
    """
    This function is used to insert/update job Logs and log details
    """
    data = get_request_form_data()
    events_data = data.pop("events", [])
    if frappe.request.method == "POST":
        if data and not data.name:
            data["doctype"] = "Logs"
            log = frappe.get_doc(data).insert()
            log_name = log.name
        else:
            log_name = data.name
        if events_data:
            for event in events_data:
                if event and event["event"]:
                    if frappe.db.exists("Code", event["event"]) and not data.name:
                        event_data = frappe.get_doc("Code", event["event"])
                        if event_data.is_billable:
                            event["is_billable"] = event_data.is_billable
                        if event_data.general_cargo_group:
                            event["general_cargo_group"] = (
                                event_data.general_cargo_group
                            )
                    if not "hold" in event or not event["hold"]:
                        event["hold"] = ""
                    event["doctype"] = "Log Details"
                    event["logs"] = log_name
                    frappe.get_doc(event).insert()
    else:
        frappe.throw("Invalid request method")


@frappe.whitelist()
def save_parent_child():
    """
    This API has been modified version of save_logs to save anykind of Doctype and Its Linked sub doctype.
    """
    data = get_request_form_data()
    child_data = data.pop("child_data", [])
    if frappe.request.method == "POST":
        if data and not data.name:
            data["doctype"] = data.doctype
            response = frappe.get_doc(data).insert()
            record_name = response.name
        else:
            record_name = data.name
        if child_data:
            for child in child_data:
                if child:
                    child["doctype"] = data.child_doctype
                    parent_name = data.doctype.lower().replace(" ", "_")
                    child[parent_name] = record_name
                    frappe.get_doc(child).insert()
    else:
        frappe.throw("Invalid request method")


@frappe.whitelist()
def save_data():
    """
    This function is used to insert/update doctype.\n
    It takes an array of records and inserts/updates them.\n
    It can be used by any doctype

    params
    ------

    :doctype
    :data
    """
    data = get_request_form_data()
    method = "POST"
    if data.doctype and data.info:
        for cur_data in json.loads(data.info):
            if "name" in cur_data and cur_data["name"]:
                doc = frappe.get_doc(data.doctype, cur_data["name"], for_update=True)
                if "flags" in cur_data:
                    del cur_data["flags"]
                if not doc.has_permission("write"):
                    frappe.throw(_("Not permitted"), frappe.PermissionError)
                doc.update(cur_data)
                doc.save()
            else:
                cur_data["doctype"] = data.doctype
                frappe.get_doc(cur_data).insert()
        frappe.db.commit()
    else:
        frappe.throw("Payload missing")


@frappe.whitelist()
def get_data():
    """
    This function returns data of provided doctype and name.\n
    The need of this function is due to the requirement of getting Link data instead \n
    of their names.
    """
    data = get_request_form_data()
    if data.doctype and data.name:
        show_hidden = data.get("show_hidden", 0)
        doc = frappe.get_doc(
            data.doctype,
            data.name,
            as_dict=True,
        )
        norm_data = get_linked_fields_data(data.doctype, doc.as_dict(), show_hidden)
        return norm_data
    else:
        frappe.throw("Payload missing")


@frappe.whitelist()
def get_job_data():
    """
    This function returns structured job data categorized into sections.
    """
    data = get_request_form_data()
    if not (data.doctype and data.name):
        frappe.throw("Payload missing")

    show_hidden = data.get("show_hidden", 0)
    doc = frappe.get_doc(data.doctype, data.name, as_dict=True)
    norm_data = get_linked_fields_data(data.doctype, doc.as_dict(), show_hidden)

    # Define mapping for sections
    sections = {
        "Job Details": [
            "billing_company",
            "job_type",
            "location",
            "acct_month",
            "acct_year",
            "coordinator",
            "sales_rep",
            "daily_guarantee",
            "demurage_rate",
            "total_tons",
            "tons_per_crane_hour",
            "job_effiencytarget",
        ],
        "Dates": [
            "eta_date",
            "etc_date",
            "date_on_schedule",
            "laycan_date",
            "laycan_end_date",
            "anchor_date",
            "dock_date_time",
            "start_date_time",
            "complete_date_time",
            "sail_date_time",
        ],
        "Ship Details": [
            "vessel_name",
            "waiting_anchorage",
            "port_origin_destination",
            "grt_dockage_yes_no",
            "grt_dockage",
            "loa_dockage_yes_no",
            "loa_dockage",
            "beam_of_vessel",
            "per_of_hold",
            "ships_gear_location",
            "no_of_barges",
            "vessel_draft_feet",
            "vessel_draft_inch",
        ],
    }

    # Create jobSections structure
    job_sections = []
    for title, fields in sections.items():
        section = {"title": title, "fields": []}
        for fieldname in fields:
            field_data = next(
                (item for item in norm_data if item["fieldname"] == fieldname), None
            )
            if field_data:
                section["fields"].append(
                    {
                        "label": field_data["label"],
                        "value": field_data["value"],
                        "type": field_data["type"],
                    }
                )
        job_sections.append(section)

    return job_sections


def get_linked_fields_data(doctype, data, show_hidden=0):
    linked_fields_data = []
    fields_to_send = [
        "total_metric_tons_from_barge_loading",
        "total_metric_tons_from_stow_planner",
        "metric_tons_difference",
        "total_metric_tons_from_customers",
    ]
    for field_name, field_value in data.items():
        field_meta = frappe.get_meta(doctype, field_name)
        fields = field_meta.fields
        result_object = get_object_by_fieldname(fields, field_name)
        if result_object:
            if (
                result_object.hidden == 1
                and (show_hidden == 0 or show_hidden == "0")
                and result_object.fieldname not in fields_to_send
            ):
                continue
            if result_object.fieldtype == "Link" and field_value:
                if frappe.__version__.startswith("14"):
                    search_widget(
                        txt="",
                        doctype=result_object.options,
                        filters={"name": field_value},
                    )
                    return_data = build_for_autosuggest(
                        frappe.response["values"], doctype=result_object.options
                    )
                    del frappe.response["values"]
                else:
                    results = search_widget(
                        txt="",
                        doctype=result_object.options,
                        filters={"name": field_value},
                        ignore_user_permissions=1,
                    )
                    return_data = build_for_autosuggest(
                        results, doctype=result_object.options
                    )
                if return_data and return_data[0] and "label" in return_data[0]:
                    # linked_fields_data[result_object.label] = return_data[0]['label']
                    linked_fields_data.append(
                        {
                            "label": result_object.label,
                            "fieldname": result_object.fieldname,
                            "value": return_data[0]["label"],
                            "type": result_object.fieldtype,
                        }
                    )
                elif return_data and return_data[0] and "description" in return_data[0]:
                    # linked_fields_data[result_object.label] = return_data[0]['label']
                    linked_fields_data.append(
                        {
                            "label": result_object.label,
                            "fieldname": result_object.fieldname,
                            "value": return_data[0]["description"],
                            "type": result_object.fieldtype,
                        }
                    )
                else:
                    linked_fields_data.append(
                        {
                            "label": result_object.label,
                            "fieldname": result_object.fieldname,
                            "value": None,
                            "type": result_object.fieldtype,
                        }
                    )
            else:
                linked_fields_data.append(
                    {
                        "label": result_object.label,
                        "fieldname": result_object.fieldname,
                        "value": field_value,
                        "type": result_object.fieldtype,
                    }
                )
    return linked_fields_data


def get_object_by_fieldname(array, target_fieldname):
    for obj in array:
        if obj.fieldname == target_fieldname:
            return obj
    return None


@frappe.whitelist()
def get_child_data():
    """
    This GET API will return child table data for provided parent id and doctype
    """
    data = get_request_form_data()
    if data.parent and data.doctype:
        response = frappe.get_all(
            data.doctype, filters={"parent": data.parent}, fields=["*"]
        )
        return response
    else:
        frappe.throw("Payload missing")


def get_meta_bundle(doctype):
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
    return bundle
