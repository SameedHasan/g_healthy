import frappe
from g_healthy.apis.api import getdoctype


@frappe.whitelist()
def getform(form_id, name=None, selectedfieldname=None, selectedfieldvalue=None):
    """
    Returns doctype fields including their metadata for multistep form\n
    Multistep form should be present in MultiStep Forms Doctype

    method
    ------
    GET

    Params
    ------
    form_id

    Response
    --------
    Object
    """
    if frappe.db.exists("MultiStep Forms", form_id):
        multistep_form = frappe.get_doc("MultiStep Forms", form_id)
        form_data = []
        if multistep_form.tabs:
            for tab in multistep_form.tabs:
                tab_data = {}
                tab_details = frappe.get_doc("Multiform Tabs", tab.tab)
                tab_data["tab_title"] = tab_details.tab_title
                tab_data["doctype"] = tab_details.doctype_name
                if (
                    form_id == "FORM-001040"
                    and selectedfieldname
                    and not selectedfieldvalue
                    and tab.tab == "FORM-TAB-001012"
                ):
                    only_send_ticket_type = True
                else:
                    only_send_ticket_type = False
                fields_information = getdoctype(
                    tab_details.doctype_name,
                    showall=True,
                    name=name,
                    selectedfieldname=selectedfieldname,
                    selectedfieldvalue=selectedfieldvalue,
                    only_send_ticket_type=only_send_ticket_type,
                )
                # return fields_information
                permissions = fields_information[0]["permissions"]
                properties_dict = {
                    prop["fieldname"]: prop
                    for prop in fields_information[0]["properties"]
                }
                result_list = []
                for item in tab_details.fields:
                    # Get the corresponding properties using the field_name
                    properties_item = properties_dict.get(item.field_name)
                    if properties_item:
                        properties_item["span"] = item.print_width
                        # Append the properties to the result_list

                        result_list.append(properties_item)
                tab_data["properties"] = result_list
                tab_data["permissions"] = permissions
                form_data.append(tab_data)
        return form_data
    else:
        frappe.throw("Form not found!")
