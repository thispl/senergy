from __future__ import unicode_literals
from frappe import _

def get_data():
    return  [
		{
			"label": _("Items and Pricing"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Product Bundle",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Item Group",
					"icon": "fa fa-sitemap",
					"label": _("Item Group"),
					"link": "Tree/Item Group",
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Price List",
				},
				{
					"type": "doctype",
					"name": "Item Price",
				},
				{
					"type": "doctype",
					"name": "Shipping Rule",
				},
				{
					"type": "doctype",
					"name": "Pricing Rule",
				},
				{
					"type": "doctype",
					"name": "Item Alternative",
				},
				{
					"type": "doctype",
					"name": "Item Manufacturer",
				},
				{
					"type": "doctype",
					"name": "Item Variant Settings",
				},
			]
		},
       
     ]
