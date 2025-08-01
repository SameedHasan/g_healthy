// Copyright (c) 2023, Sameed Hasan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Page Tabs', {
	refresh: function(frm) {
        // Triggered when the form is loaded or refreshed
		fetchFields(frm);
        frm.fields_dict['route'].get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                }
            };
        };

        frm.fields_dict['menu_item'].get_query = function(doc, cdt, cdn) {
            return {
                filters: {
                }
            };
        };

        frm.fields_dict['route'].df.onchange = function() {
            fetchFields(frm);
        };
        frm.fields_dict['menu_item'].df.onchange = function() {
            fetchFields(frm);
        };
    },
    view: function(frm) {
        if(frm.doc.view == "Custom View")
        {
            frm.set_df_property('button_type', 'options', 'Custom Button\nNone');
        }
        else
        {
            frm.set_df_property('button_type', 'options', 'Add Button\nCustom Button\nNone');
        }
    }
});

function fetchFields(frm) {
    if(frm.doc.route)
    {
        var linkedDocType = frm.doc.parent_doctype || frm.doc.parent_doctype_1;
    }
    else if(frm.doc.menu_item)
    {
        var linkedDocType = frm.doc.parent_doctype_1;
    }
    else
    {
        var linkedDocType = frm.doc.parent_doctype;
    }
    if (linkedDocType) {
        frappe.model.with_doctype(linkedDocType, function() {
            var fields = frappe.get_meta(linkedDocType).fields;
			var fieldOptions = [];
            fields.forEach(function(field) {
                if (field.fieldtype !== 'Table') {
                    fieldOptions.push(field.fieldname);
                }
            });
			var desctiption_data = "EXAMPLE:{fieldname1}-{fieldname2}<br>"
			desctiption_data +=  "<b>Fields:</b> " + fieldOptions.join(', ')
			frm.set_df_property('heading', 'description', desctiption_data);
			frm.set_df_property('second_field', 'options', fieldOptions.join('\n'));
			frm.set_df_property('third_field', 'options', fieldOptions.join('\n'));
        });
    }
}
