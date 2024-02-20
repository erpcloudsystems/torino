app_name = "torino"
app_title = "Torino"
app_publisher = "ECS"
app_description = "customization"
app_email = "info@erpcloud.systems"
app_license = "mit"


doc_events = {
		"Payment Entry": {
		"before_insert": "torino.doctype_triggers.accounting.payment_entry.payment_entry.before_insert",
		"after_insert": "torino.doctype_triggers.accounting.payment_entry.payment_entry.after_insert",
		"onload": "torino.doctype_triggers.accounting.payment_entry.payment_entry.onload",
		"before_validate": "torino.doctype_triggers.accounting.payment_entry.payment_entry.before_validate",
		"validate": "torino.doctype_triggers.accounting.payment_entry.payment_entry.validate",
		"on_submit": "torino.doctype_triggers.accounting.payment_entry.payment_entry.on_submit",
		"on_cancel": "torino.doctype_triggers.accounting.payment_entry.payment_entry.on_cancel",
		"on_update_after_submit": "torino.doctype_triggers.accounting.payment_entry.payment_entry.on_update_after_submit",
		"before_save": "torino.doctype_triggers.accounting.payment_entry.payment_entry.before_save",
		"before_cancel": "torino.doctype_triggers.accounting.payment_entry.payment_entry.before_cancel",
		"on_update": "torino.doctype_triggers.accounting.payment_entry.payment_entry.on_update",
	}}

doctype_js = {
	"Payment Entry" : "doctype_triggers/accounting/payment_entry/payment_entry.js"
}
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/torino/css/torino.css"
# app_include_js = "/assets/torino/js/torino.js"

# include js, css files in header of web template
# web_include_css = "/assets/torino/css/torino.css"
# web_include_js = "/assets/torino/js/torino.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "torino/public/scss/website"

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
# app_include_icons = "torino/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "torino.utils.jinja_methods",
#	"filters": "torino.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "torino.install.before_install"
# after_install = "torino.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "torino.uninstall.before_uninstall"
# after_uninstall = "torino.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "torino.utils.before_app_install"
# after_app_install = "torino.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "torino.utils.before_app_uninstall"
# after_app_uninstall = "torino.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "torino.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Payroll Entry": "torino.overrides.payroll_entry.payroll_entry.CustomPayrollEntry"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"torino.tasks.all"
#	],
#	"daily": [
#		"torino.tasks.daily"
#	],
#	"hourly": [
#		"torino.tasks.hourly"
#	],
#	"weekly": [
#		"torino.tasks.weekly"
#	],
#	"monthly": [
#		"torino.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "torino.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "torino.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "torino.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["torino.utils.before_request"]
# after_request = ["torino.utils.after_request"]

# Job Events
# ----------
# before_job = ["torino.utils.before_job"]
# after_job = ["torino.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"torino.auth.validate"
# ]
