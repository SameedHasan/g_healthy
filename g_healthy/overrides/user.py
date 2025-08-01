import frappe
from frappe import _
from frappe.core.doctype.user.user import User
from frappe.utils import now_datetime
from frappe.utils.data import sha256_hash
from frappe.utils.password import get_password_reset_limit
from g_healthy.rate_limiter import rate_limit


class CustomUser(User):

    def reset_password(self, send_email=False, password_expired=False):
        from frappe.utils import get_url

        key = frappe.generate_hash()
        hashed_key = sha256_hash(key)
        self.db_set("reset_password_key", hashed_key)
        self.db_set("last_reset_password_key_generated_on", now_datetime())

        url = "dashboard/update-password?key=" + key
        if password_expired:
            url = "dashboard/update-password?key=" + key + "&password_expired=true"

        link = get_url(url, allow_header_override=False)
        if send_email:
            self.password_reset_mail(link)

        return link


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=get_password_reset_limit, seconds=60 * 60)
def custom_reset_password(user: str) -> str:
    try:
        user: User = frappe.get_doc("User", user)
        if user.name == "Administrator":
            return "not allowed"
        if not user.enabled:
            return "disabled"

        user.validate_reset_password()
        user.reset_password(send_email=True)

        return frappe.msgprint(
            msg=_("Password reset instructions have been sent to your email"),
            title=_("Password Email Sent"),
        )
    except frappe.DoesNotExistError:
        frappe.local.response["http_status_code"] = 404
        frappe.clear_messages()
        return "not found"
