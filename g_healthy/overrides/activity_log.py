import frappe
from frappe.core.doctype.activity_log.activity_log import ActivityLog


class CustomActivityLog(ActivityLog):
    def before_insert(self):
        if (
            "Session Expired" in self.subject
            or "Force Logged out by the user" in self.subject
        ):
            activity_logs = frappe.get_all(
                "Activity Log",
                filters={"logout_time": ["=", None], "custom_log": ["=", "True"]},
                fields=["*"],
            )
            if activity_logs:
                for log in activity_logs:
                    session_id = log.session_id
                    existing_session = frappe.cache().hget("session", session_id)
                    if not existing_session:
                        activity_log = frappe.get_doc("Activity Log", log.name)
                        activity_log.logout_time = frappe.utils.now_datetime()
                        activity_log.save(ignore_permissions=True)
                        frappe.db.commit()
