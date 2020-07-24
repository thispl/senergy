# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		# {
		# 	"module_name": "Senergy",
		# 	"color": "grey",
		# 	"icon": "octicon octicon-file-directory",
		# 	"type": "module",
		# 	"label": _("Senergy")
		# },
		{
			"module_name": "Item Master",
			"category": "Modules",
			"label": _("Item Master"),
			"color": "#f39c12",
			"icon": "fa fa-check-circle",
			"type": "module",
			"description": "item list"
			# "onboard_present": 1
		},
		{
			"module_name": "Senergy",
			"category": "Modules",
			"label": _("Inventory Management"),
			"color": "#f39c12",
			"icon": "fa fa-cubes",
			"type": "module",
			"description": "Inventory Management",
			"onboard_present": 1
		},
		{
			"module_name": "Fixed Assets",
			"category": "Modules",
			"label": _("Assets Management"),
			"color": "#f39c12",
			"icon": "fa fa-desktop",
			"type": "module",
			"description": "Assets Management"
			# "onboard_present": 1
		}
	]
