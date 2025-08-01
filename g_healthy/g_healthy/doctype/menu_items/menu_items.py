# Copyright (c) 2023, Sameed Hasan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class MenuItems(Document):
    def validate(self):
        if not validate_route(self.path):
            frappe.throw("Path is not valid. Do not use special characters")
        # if frappe.db.exists("Menu Items", {"route": self.route, "order_sequence": self.order_sequence, "name": ["!=", self.name]}) and self.route != 0:
        #     frappe.throw('Order already exists for this route')


def validate_route(text):
    # Check if the text starts with '/'
    if text.startswith("/"):
        return False

    # Check if there is exactly one '/' in the text
    if text.count("/") != 0:
        return False

    # Check if there are no special characters in the text
    if not re.match("^[a-zA-Z0-9/ ]*$", text):
        return False

    return True


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
    cur_roles = frappe.get_roles(frappe.session.user)
    child = frappe.get_all(
        "RoutesRoles",
        fields=["*"],
        filters={"title": ["IN", cur_roles], "parenttype": "Menu Items"},
    )
    child = [row["parent"] for row in child]
    # Iterate through the input data
    for item in input_data:
        if item.get("name") in child:

            temp_menu = frappe.get_doc("Menu Items", item.get("name"))
            roles2 = temp_menu.roles
            roles_temp = []
            if roles2:
                for role_temp in roles2:
                    roles_temp.append(role_temp.title)
            name = item.get("name")
            tabs = frappe.get_all(
                "Page Tabs",
                filters={"menu_item": name},
                fields=["*"],
                order_by="sequence_number asc",
            )
            if tabs:
                for tab in tabs:
                    permissions_r = None
                    if tab.page:
                        roles1 = frappe.get_roles(frappe.session.user)
                        keys = []
                        link_keys = []
                        try:
                            fields = None
                            docs = get_meta_bundle(tab.page)
                            if docs and docs[0]:
                                fields = docs[0].fields
                                permissions = docs[0].permissions
                                if permissions:
                                    for permission in permissions:
                                        if permission.permlevel == 0:
                                            if "Administrator" in roles1:
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

                        except frappe.DoesNotExistError:
                            frappe.clear_messages()
                    tab["permissions"] = permissions_r
            key = item.get("path")
            label = item.get("label")
            content = item.get("content")
            groupby = item.get("group_by")
            page = item.get("page")
            child_page = item.get("child_page")

            form_title = item.get("form_title")
            update_form_title = item.get("update_form_title")
            add_button_title = item.get("add_button_title")
            cancel_button_title = item.get("cancel_button_title")
            update_button_title = item.get("update_button_title")
            add_button_type = item.get("add_button_type")
            template = item.get("template")

            if groupby:
                # If the item has a "groupby" value, add it to the grouped_data array
                grouped_data.append(
                    {
                        "key": key,
                        "label": label,
                        "content": content,
                        "groupby": groupby,
                        "page": page,
                        "child_page": child_page,
                        "name": name,
                        "labels": {
                            "form_title": form_title,
                            "update_form_title": update_form_title,
                            "add_button_title": add_button_title,
                            "cancel_button_title": cancel_button_title,
                            "update_button_title": update_button_title,
                            "add_button_type": add_button_type,
                            "template": template,
                        },
                        "tabs": tabs,
                        "roles": roles_temp,
                    }
                )
            else:
                # If there's no "groupby" value, add it to the ungrouped_data array
                ungrouped_data.append(
                    {
                        "key": key,
                        "label": label,
                        "content": content,
                        "page": page,
                        "child_page": child_page,
                        "name": name,
                        "labels": {
                            "form_title": form_title,
                            "update_form_title": update_form_title,
                            "add_button_title": add_button_title,
                            "cancel_button_title": cancel_button_title,
                            "update_button_title": update_button_title,
                            "add_button_type": add_button_type,
                            "template": template,
                        },
                        "tabs": tabs,
                        "roles": roles_temp,
                    }
                )

    # Iterate through ungrouped_data and add items from grouped_data to their submenu
    for ungrouped_item in ungrouped_data:
        key = ungrouped_item.get("name")
        ungrouped_item["subMenu"] = [
            grouped_item
            for grouped_item in grouped_data
            if grouped_item.get("groupby") == key
        ]

    return modify_submenu_data(ungrouped_data)


@frappe.whitelist()
def get_menu_items(parent_id):
    try:
        # Fetch the data
        tabs = frappe.get_all(
            "Menu Items",
            filters={"route": parent_id},
            fields=[
                "name",
                "order_sequence",
                "path",
                "label",
                "content",
                "group_by",
                "page",
                "child_page",
                "creation",
                "form_title",
                "update_form_title",
                "add_button_title",
                "cancel_button_title",
                "update_button_title",
                "add_button_type",
                "template",
            ],
            order_by="order_sequence asc",
        )

        return transform_tabs_data(tabs)
    except Exception as e:
        frappe.log_error(f"Error in get_tabs_menu_by_parent: {str(e)}")
        return None


@frappe.whitelist()
def get_menu_items_optimized(parent_id):
    """
    Optimized version of get_menu_items that uses batch queries to reduce database calls
    """
    try:
        # Fetch the data
        tabs = frappe.get_all(
            "Menu Items",
            filters={"route": parent_id},
            fields=[
                "name",
                "order_sequence",
                "path",
                "label",
                "content",
                "group_by",
                "page",
                "child_page",
                "creation",
                "form_title",
                "update_form_title",
                "add_button_title",
                "cancel_button_title",
                "update_button_title",
                "add_button_type",
                "template",
            ],
            order_by="order_sequence asc",
        )

        return transform_tabs_data_optimized(tabs)
    except Exception as e:
        frappe.log_error(f"Error in get_menu_items_optimized: {str(e)}")
        return None


def transform_tabs_data_optimized(input_data):
    """
    Optimized version of transform_tabs_data that uses batch queries
    """
    grouped_data = []  # Array to store objects with "groupby"
    ungrouped_data = []  # Array to store objects without "groupby"
    cur_roles = frappe.get_roles(frappe.session.user)

    # OPTIMIZED: Batch fetch all menu item roles at once
    menu_item_names = [item.get("name") for item in input_data]
    all_menu_roles = frappe.get_all(
        "RoutesRoles",
        fields=["*"],
        filters={
            "title": ["IN", cur_roles],
            "parenttype": "Menu Items",
            "parent": ["IN", menu_item_names],
        },
    )
    authorized_menu_items = {row["parent"] for row in all_menu_roles}

    # OPTIMIZED: Batch fetch all tabs for all menu items at once
    all_tabs = frappe.get_all(
        "Page Tabs",
        filters={"menu_item": ["IN", menu_item_names]},
        fields=["*"],
        order_by="sequence_number asc",
    )

    # Group tabs by menu item
    tabs_lookup = {}
    for tab in all_tabs:
        if tab["menu_item"] not in tabs_lookup:
            tabs_lookup[tab["menu_item"]] = []
        tabs_lookup[tab["menu_item"]].append(tab)

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

    # Iterate through the input data
    for item in input_data:
        if item.get("name") in authorized_menu_items:
            # Get menu item roles using the original approach
            temp_menu = frappe.get_doc("Menu Items", item.get("name"))
            roles2 = temp_menu.roles
            roles_temp = []
            if roles2:
                for role_temp in roles2:
                    roles_temp.append(role_temp.title)

            name = item.get("name")
            # Use pre-fetched tabs
            tabs = tabs_lookup.get(name, [])

            if tabs:
                for tab in tabs:
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

            key = item.get("path")
            label = item.get("label")
            content = item.get("content")
            groupby = item.get("group_by")
            page = item.get("page")
            child_page = item.get("child_page")

            form_title = item.get("form_title")
            update_form_title = item.get("update_form_title")
            add_button_title = item.get("add_button_title")
            cancel_button_title = item.get("cancel_button_title")
            update_button_title = item.get("update_button_title")
            add_button_type = item.get("add_button_type")
            template = item.get("template")

            if groupby:
                # If the item has a "groupby" value, add it to the grouped_data array
                grouped_data.append(
                    {
                        "key": key,
                        "label": label,
                        "content": content,
                        "groupby": groupby,
                        "page": page,
                        "path": key,
                        "child_page": child_page,
                        "name": name,
                        "labels": {
                            "form_title": form_title,
                            "update_form_title": update_form_title,
                            "add_button_title": add_button_title,
                            "cancel_button_title": cancel_button_title,
                            "update_button_title": update_button_title,
                            "add_button_type": add_button_type,
                            "template": template,
                        },
                        "tabs": tabs,
                        "roles": roles_temp,
                    }
                )
            else:
                # If there's no "groupby" value, add it to the ungrouped_data array
                ungrouped_data.append(
                    {
                        "key": key,
                        "label": label,
                        "content": content,
                        "page": page,
                        "path": key,
                        "child_page": child_page,
                        "name": name,
                        "labels": {
                            "form_title": form_title,
                            "update_form_title": update_form_title,
                            "add_button_title": add_button_title,
                            "cancel_button_title": cancel_button_title,
                            "update_button_title": update_button_title,
                            "add_button_type": add_button_type,
                            "template": template,
                        },
                        "tabs": tabs,
                        "roles": roles_temp,
                    }
                )

    # Iterate through ungrouped_data and add items from grouped_data to their submenu
    for ungrouped_item in ungrouped_data:
        key = ungrouped_item.get("name")
        ungrouped_item["subMenu"] = [
            grouped_item
            for grouped_item in grouped_data
            if grouped_item.get("groupby") == key
        ]

    return modify_submenu_data(ungrouped_data)


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
