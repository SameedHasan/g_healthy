// Copyright (c) 2023, Sameed Hasan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Menu Items', {
	// refresh: function(frm) {

	// }
	setup: function(frm) {
		frm.set_query("group_by", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Menu Items', 'is_group', '=', 1]
				]
			};
		});
	},
});
