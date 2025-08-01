app_name = "g_healthy"
app_title = "G Healthy"
app_publisher = "Sameed Hasan"
app_description = "Bump App "
app_email = "sameedh41@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "g_healthy",
# 		"logo": "/assets/g_healthy/logo.png",
# 		"title": "G Healthy",
# 		"route": "/g_healthy",
# 		"has_permission": "g_healthy.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/g_healthy/css/g_healthy.css"
# app_include_js = "/assets/g_healthy/js/g_healthy.js"

# include js, css files in header of web template
# web_include_css = "/assets/g_healthy/css/g_healthy.css"
# web_include_js = "/assets/g_healthy/js/g_healthy.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "g_healthy/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "g_healthy/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "g_healthy.utils.jinja_methods",
# 	"filters": "g_healthy.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "g_healthy.install.before_install"
# after_install = "g_healthy.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "g_healthy.uninstall.before_uninstall"
# after_uninstall = "g_healthy.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "g_healthy.utils.before_app_install"
# after_app_install = "g_healthy.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "g_healthy.utils.before_app_uninstall"
# after_app_uninstall = "g_healthy.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "g_healthy.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"g_healthy.tasks.all"
# 	],
# 	"daily": [
# 		"g_healthy.tasks.daily"
# 	],
# 	"hourly": [
# 		"g_healthy.tasks.hourly"
# 	],
# 	"weekly": [
# 		"g_healthy.tasks.weekly"
# 	],
# 	"monthly": [
# 		"g_healthy.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "g_healthy.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "g_healthy.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "g_healthy.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["g_healthy.utils.before_request"]
# after_request = ["g_healthy.utils.after_request"]

# Job Events
# ----------
# before_job = ["g_healthy.utils.before_job"]
# after_job = ["g_healthy.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"g_healthy.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

