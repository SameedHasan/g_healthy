// Copyright (c) 2023, Sameed Hasan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Multiform Tabs', {
    onload: function(frm) {
        if (frm.doc.doctype_name) {
            fetchFields(frm);
        }
    },
	refresh: function(frm) {
		frm.fields_dict['doctype_name'].df.onchange = function() {
            fetchFields(frm);
        };
	}
});

function fetchFields(frm) {
    var linkedDocType = frm.doc.doctype_name;
    if (linkedDocType) {
        frappe.model.with_doctype(linkedDocType, function() {
            var fields = frappe.get_meta(linkedDocType).fields;
			var fieldOptions = [];
            fields.forEach(function(field) {
                if (field.fieldtype !== 'Table') {
                    fieldOptions.push(field.fieldname);
                }
            });
            var field_name = frappe.meta.get_docfield("Multiform Tab Fields","field_name", frm.doc.name);
            field_name.options = fieldOptions.join('\n');
        });
    }
}
