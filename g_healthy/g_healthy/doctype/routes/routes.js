// Copyright (c) 2023, Sameed Hasan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Routes", {
  refresh: function (frm) {
    // Add a custom button to trigger the method
    var pageView = frm.doc.page_view;
    if (pageView === "List") {
      // Show and make the "Page" field required
      frm.toggle_display("page", true);
      frm.set_df_property("page", "reqd", 1);
    } else {
      // Hide and make the "Page" field not required
      frm.toggle_display("page", false);
      frm.set_df_property("page", "reqd", 0);
    }
    // frm.toggle_display("page", true);
    // frm.set_df_property("page", "reqd", 0);
    frm.add_custom_button(__("Get Parent and Child Data"), function () {
      frappe.call({
        method:
          "g_healthy.g_healthy.doctype.routes.api.get_tabs_menu_by_parent", // Adjust this path
        args: { parent_id: frm.doc.name },
        callback: function (response) {
          // Process the retrieved data here
          var data = response.message;
          // Handle the data as needed
        },
      });
    });
  },
  page_view: function (frm) {
    // Get the value of the "Page View" field
    var pageView = frm.doc.page_view;

    // Check if the selected value is "List"
    if (pageView === "List") {
      // Show and make the "Page" field required
      frm.toggle_display("page", true);
      frm.set_df_property("page", "reqd", 1);
    } else {
      // Hide and make the "Page" field not required
      frm.toggle_display("page", false);
      frm.set_df_property("page", "reqd", 0);
    }
  },
});
