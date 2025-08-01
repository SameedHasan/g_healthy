import json

import frappe
from frappe import get_all

from ..menu_items.menu_items import get_menu_items, get_menu_items_optimized


@frappe.whitelist()
def get_parent_and_child_data():
    cur_roles = frappe.get_roles(frappe.session.user)
    child = get_all(
        "RoutesRoles",
        fields=["parent"],
        filters={"title": ["IN", cur_roles], "parenttype": "Routes"},
    )
    child = [row["parent"] for row in child]
    data = get_all(
        "Routes",
        fields=["*"],
        filters={"ishidden": 0, "name": ["IN", child]},
        order_by="sequence_number asc",
    )

    # OPTIMIZED: Batch fetch all roles for all routes at once
    route_names = [row["name"] for row in data]
    all_roles = get_all(
        "RoutesRoles",
        filters={"parent": ["IN", route_names]},
        fields=["parent", "title"],
    )

    # Create a lookup dictionary for roles
    roles_lookup = {}
    for role in all_roles:
        if role["parent"] not in roles_lookup:
            roles_lookup[role["parent"]] = []
        roles_lookup[role["parent"]].append(role["title"])

    # OPTIMIZED: Batch fetch all tabs for all routes at once
    all_tabs = get_all(
        "Page Tabs",
        filters={"route": ["IN", route_names]},
        fields=["*"],
        order_by="sequence_number asc",
    )

    # Group tabs by route
    tabs_lookup = {}
    for tab in all_tabs:
        if tab["route"] not in tabs_lookup:
            tabs_lookup[tab["route"]] = []
        tabs_lookup[tab["route"]].append(tab)

    # OPTIMIZED: Batch fetch all unique pages for meta bundle caching
    unique_pages = set()
    for tab in all_tabs:
        if tab.get("page"):
            unique_pages.add(tab["page"])

    # Pre-load meta bundles for all unique pages
    meta_bundle_cache = {}
    for page in unique_pages:
        try:
            meta_bundle_cache[page] = get_meta_bundle(page)
        except:
            meta_bundle_cache[page] = None

    # Include child table data by querying the child table directly
    for row in data:
        # Use pre-fetched roles
        row["roles"] = roles_lookup.get(row["name"], [])

        # Use pre-fetched tabs
        tabs = tabs_lookup.get(row["name"], [])

        if tabs:
            for tab in tabs:
                # Get tab details using the original approach for roles
                tab_details = frappe.get_doc("Page Tabs", tab["name"])
                roles_temp = []
                if tab_details.roles:
                    for role_temp in tab_details.roles:
                        roles_temp.append(role_temp.title)
                tab["roles"] = roles_temp

                permissions_r = None
                if tab.get("page") and tab["page"] in meta_bundle_cache:
                    docs = meta_bundle_cache[tab["page"]]
                    if docs and docs[0]:
                        permissions = docs[0].permissions
                        if permissions:
                            for permission in permissions:
                                if permission.permlevel == 0:
                                    if "Administrator" in cur_roles:
                                        permissions_r = {
                                            "read": 1,
                                            "create": 1,
                                            "delete": 1,
                                            "update": 1,
                                            "only_owner": 0,
                                        }
                                    else:
                                        permissions_r = {
                                            "read": permission.read,
                                            "create": permission.create,
                                            "delete": permission.delete,
                                            "update": permission.write,
                                            "only_owner": permission.if_owner,
                                        }
                tab["permissions"] = permissions_r

        # Add header data here - use optimized function to reduce database calls
        row["subRoutes"] = get_menu_items_optimized(row["name"])
        row["tabs"] = tabs

    # Sort the data array by the "name" field
    # sorted_data = sorted(data, key=lambda x: x["name"])
    sorted_data = sorted(data, key=lambda x: x["sequence_number"])

    return sorted_data


@frappe.whitelist()
def modify_submenu_data(data):
    # Iterate through the data and modify the "subMenu" and "content" fields
    modified_data = []
    for item in data:
        sub_menu = item.get("subMenu", [])

        # Remove the "subMenu" field if it's an empty list
        if not sub_menu:
            item.pop("subMenu", None)
        else:
            # Remove the "content" field if "subMenu" is not an empty list
            item.pop("content", None)

        # Add the modified item to the result
        modified_data.append(item)

    return modified_data


@frappe.whitelist()
def transform_tabs_data(input_data):
    grouped_data = []  # Array to store objects with "groupby"
    ungrouped_data = []  # Array to store objects without "groupby"

    # Iterate through the input data
    for item in input_data:
        key = item.get("key")
        label = item.get("label")
        content = item.get("content")
        groupby = item.get("groupby")
        page = item.get("page")

        if groupby:
            # If the item has a "groupby" value, add it to the grouped_data array
            grouped_data.append(
                {
                    "key": key,
                    "label": label,
                    "content": content,
                    "groupby": groupby,
                    "page": page,
                }
            )
        else:
            # If there's no "groupby" value, add it to the ungrouped_data array
            ungrouped_data.append(
                {"key": key, "label": label, "content": content, "page": page}
            )

    # Iterate through ungrouped_data and add items from grouped_data to their submenu
    for ungrouped_item in ungrouped_data:
        key = ungrouped_item.get("key")
        ungrouped_item["subMenu"] = [
            grouped_item
            for grouped_item in grouped_data
            if grouped_item.get("groupby") == key
        ]

    return modify_submenu_data(ungrouped_data)


@frappe.whitelist()
def get_tabs_menu_by_parent(parent_id):
    try:
        # Fetch the data
        tabs = frappe.get_all(
            "Page Tabs",
            filters={"parent": parent_id},
            fields=["name", "key", "label", "content", "groupby", "page", "creation"],
            order_by="creation desc",
        )

        # Sort the tabs data if needed
        # sorted_tabs = sorted(tabs, key=lambda x: x["key"])
        # sorted_data = sorted(tabs, key=lambda x: x["creation"], reverse=True)
        # return tabs
        return transform_tabs_data(tabs)
        # return tabs
    except Exception as e:
        frappe.log_error(f"Error in get_tabs_menu_by_parent: {str(e)}")
        return None


@frappe.whitelist()
def get_doctype_fields_and_data(doctype):
    # Check if the DocType exists
    if not frappe.db.exists("DocType", doctype):
        return {"error": "DocType not found"}

    # Get the fields of the DocType
    meta = frappe.get_meta(doctype)
    fields = meta.fields

    # Define the fieldnames and separate lists for table and multiselect fields
    fieldnames = ["name"]
    table_fields = []
    table_multiselect_fields = []

    for field in fields:
        if field.fieldtype not in ["Table", "Table MultiSelect"]:
            fieldnames.append(field.fieldname)
        elif field.fieldtype == "Table":
            table_fields.append(field.fieldname)
        elif field.fieldtype == "Table MultiSelect":
            table_multiselect_fields.append(
                {"fieldname": field.fieldname, "child_table_name": field.options}
            )

    # Construct the custom SQL query dynamically
    fieldnames_str = ", ".join([f"`{fieldname}`" for fieldname in fieldnames])
    custom_query = f"SELECT {fieldnames_str} FROM `tab{doctype}`"

    # Execute the query and fetch the data
    data = frappe.db.sql(custom_query, as_dict=True)

    # Iterate through the data and fetch data from child tables
    for record in data:
        for field_info in table_multiselect_fields:
            child_table_name = field_info["child_table_name"]
            child_table_field = field_info["fieldname"]
            parent_name = record["name"]

            # Fetch data from the child table where parent is data.name
            child_table_data = frappe.get_all(
                child_table_name,
                filters={"parent": parent_name},
                fields=["company_title"],
            )
            record[child_table_field] = child_table_data

    # Update the fieldnames with multiselect fieldnames
    fieldnames += [field_info["fieldname"] for field_info in table_multiselect_fields]

    # Create a dictionary to hold fieldnames and data
    result = {
        "keys": fieldnames,
        "values": data,
        "table_fields": table_fields,
        "table_multiselect_fields": table_multiselect_fields,
    }

    return result


# Api to Generate JSON For React Forms
def get_optional(field):
    if field.reqd:
        return False
    else:
        return True


def get_field_type_definition(field, doctype):
    enum = {}
    if field.fieldtype == "Select":
        enum = get_select_field_options(field)

    if enum:
        res = {
            "title": field.fieldname,
            "type": get_field_type(field, doctype),
            "enum": enum,
        }
    else:
        res = {
            "title": field.fieldname,
            "type": get_field_type(field, doctype),
        }
    return res


def get_field_type(field, doctype):
    basic_fieldtypes = {
        "Data": "string",
        "Text Editor": "string",
        "Text": "string",
        "Code": "string",
        "Link": "string",
        "Dynamic Link": "string",
        "Read Only": "string",
        "Password": "string",
        "Check": "0 | 1",
        "Int": "number",
        "Float": "number",
        "Currency": "number",
        "Percent": "number",
        "Attach Image": "string",
        "Attach": "string",
        "HTML Editor": "string",
        "Image": "string",
        "Duration": "string",
        "Small Text": "string",
        "Date": "date",
        "Datetime": "string",
        "Time": "string",
        "Phone": "string",
        "Color": "string",
        "Long Text": "string",
        "Markdown Editor": "string",
        "Select": "string",
    }

    if field.fieldtype == "Select":
        if field.options:
            options = field.options.split("\n")
            enum_values = [option.strip() for option in options]
            return "string"
        else:
            return "string"

    if field.fieldtype in basic_fieldtypes:
        return basic_fieldtypes[field.fieldtype]
    else:
        return "any"


def get_select_field_options(field):
    if field.options:
        options = field.options.split("\n")
        enum_values = [
            option.strip() for option in options
        ]  # Remove leading/trailing whitespace
        return enum_values


@frappe.whitelist()
def get_doctype_fields(doctype_name):
    # Check if the DocType exists
    if not frappe.get_meta(doctype_name).get("issingle"):
        doctype = frappe.get_meta(doctype_name)
        content_object = {
            "title": doctype_name,
            "description": "Form description",
            "type": "object",
            "required": [],
            "properties": {},
        }

        for field in doctype.fields:
            if field.fieldtype in [
                "Section Break",
                "Column Break",
                "HTML",
                "Button",
                "Fold",
                "Heading",
                "Tab Break",
                "Break",
            ]:
                continue
            if get_optional(field):
                content_object["properties"][field.fieldname] = (
                    get_field_type_definition(field, doctype)
                )
            else:
                content_object["properties"][field.fieldname] = (
                    get_field_type_definition(field, doctype)
                )
                content_object["required"].append(field.fieldname)

        return json.dumps(content_object)

    return json.dumps({"error": "Doctype not found."})


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
