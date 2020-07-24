# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "senergy"
app_title = "Senergy"
app_publisher = "TeamPRO"
app_description = "Inventory Management"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "barathprathosh@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/senergy/css/senergy.css"
app_include_js = "/assets/js/senergy.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/senergy/css/senergy.css"
# web_include_js = "/assets/senergy/js/senergy.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "senergy.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "senergy.install.before_install"
# after_install = "senergy.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "senergy.notifications.get_notification_config"

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

doc_events = {
	"Asset Maintenance Log": {
		"on_submit": "senergy.custom.maintenance_completion_mail"
    }
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    # "Stock Entry":{
    #     "on_submit": "senergy.custom.minimum_stock_alert"
    # }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"senergy.tasks.all"
	# ],
	"daily": [
		"senergy.custom.maintenance_due_date_alert"
	],
# 	"hourly": [
# 		"senergy.tasks.hourly"
# 	],
# 	"weekly": [
# 		"senergy.tasks.weekly"
# 	]
# 	"monthly": [
# 		"senergy.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "senergy.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "senergy.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "senergy.task.get_dashboard_data"
# }

