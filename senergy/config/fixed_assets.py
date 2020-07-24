from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():
    return  [
		{
			"label": _("Assets Management"),
			"items": [
				{
					"type": "doctype",
					"name": "Asset",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Asset Movement",
					"onboard": 1,
					"description": _("Transfer an asset from one warehouse to another")
				},
			]
		},
		{
			"label": _("Asset Maintenance"),
			"items": [
				{
					"type": "doctype",
					"name": "Asset Maintenance Team",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Asset Maintenance",
					"onboard": 1,
					"dependencies": ["Asset Maintenance Team"],
				},
				{
					"type": "doctype",
					"name": "Asset Maintenance Tasks",
					"onboard": 1,
					"dependencies": ["Asset Maintenance"],
				},
				{
					"type": "doctype",
					"name": "Asset Maintenance Log",
					"onboard": 1,
					"dependencies": ["Asset Maintenance"],
				},
				{
					"type": "doctype",
					"name": "Asset Value Adjustment",
					"onboard": 1,
					"dependencies": ["Asset"],
				},
				{
					"type": "doctype",
					"name": "Asset Repair",
					"onboard": 1,
					"dependencies": ["Asset"],
				},
			]
		},
		{
			"label": _("Asset Reports"),
			"icon": "fa fa-table",
			"items": [
				{
					"type": "report",
					"name": "Fixed Asset Register",
					"onboard": 1,
					"doctype": "Asset",
					"is_query_report": True,
					"dependencies": ["Asset"],
				},
				{
					"type": "report",
					"name": "Asset Depreciations and Balances",
					"onboard": 1,
					"doctype": "Asset",
					"is_query_report": True,
					"dependencies": ["Asset"],
				},
				{
					"type": "report",
					"name": "Asset Maintenance",
					"onboard": 1,
					"doctype": "Asset Maintenance",
					"dependencies": ["Asset Maintenance"]
				},
			]
		}
       
     ]
