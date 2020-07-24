from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():
    return  [
		{
			"label": _("Main Menu"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Monitoring Panel",
					"doctype": "Stock Ledger Entry",
					"onboard": 1,
					"dependencies": ["Item"],
                    "label": _("Monitoring Panel")
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "Pending Requests",
					"doctype": "Material Request",
					"dependencies": ["Item"],
					"onboard": 1,
					"route":"#List/Material Request/Report/Pending Requests",
                    "label": _("Pending Requests")
				}
			]
		},
        
        {
			"label": _("Action Items"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"onboard": 1,
                    "route": "#Form/Item/New Item 1",
                    "label":_("Add Items")
				},
                {
					"type": "doctype",
					"name": "Item",
					"onboard": 1,
                    "label":_("Edit Items")
				},
                {
					"type": "doctype",
					"name": "Stock Entry",
					"onboard": 1,
                    "reference_doctype": "Stock Entry",
                    "dependencies": ["Item"],
                    "route":"#List/Stock Entry/List?stock_entry_type=Material Receipt",
                    "label":_("Recieving Items")
				},
                 {
					"type": "doctype",
					"name": "Stock Entry",
					"onboard": 1,
                    "route":"#List/Stock Entry/List?stock_entry_type=Material Transfer",
                    "dependencies": ["Item"],
                    "label":_("Moving Items")
				},
                {
					"type": "doctype",
					"name": "Freezing Request",
                    "dependencies": ["Item"],
					"onboard": 1,
					"route":"#List/Freezing Request/List",
                    "label":_("Disabling Items")
				},
                {
					"type": "doctype",
					"name": "Item",
					"onboard": 1,
                    "dependencies": ["Item"],
                    "label":_("Disposing Items")
				},
                {
					"type": "doctype",
					"name": "Item",
					"route": "#List/Stock Reconciliation/List",
					"onboard": 1,
                    "label":_("Physical Count Reconciliation")
				},
			]
		},
		{
			"label": _("Purchase"),
			"items": [
				{
					"type": "doctype",
					"name": "Material Request",
					"onboard": 1,
                    "label":_("Material Request"),
					"dependencies": ["Item"],
				},
               {
					"type": "doctype",
					"name": "Purchase Order",
					"onboard": 1,
                    "label":_("Purchase Order"),
					"dependencies": ["Supplier"],
				},
				{
					"type": "doctype",
					"name": "Purchase Receipt",
					"onboard": 1,
                    "label":_("Purchase Receipt"),
					"dependencies": ["Supplier"],
				},
				{
					"type": "doctype",
					"name": "Landed Cost Voucher",
					"onboard": 1,
                    "label":_("Landed Cost Voucher"),
					"dependencies": ["Purchase Receipt"],
				},
				{
					"type": "doctype",
					"name": "Supplier",
					"onboard": 1,
                    "label":_("Supplier"),
				},
				{
					"type": "doctype",
					"name": "Request for Quotation",
					"onboard": 1,
                    "label":_("Request for Quotation"),
				},
				{
					"type": "doctype",
					"name": "Supplier Quotation",
					"onboard": 1,
                    "label":_("Supplier Quotation"),
				}
			]
		},
        {
			"label": _("Stock Reports"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Item Additions Report",
					"doctype": "Item",
					"route":"List/Item/Report/Item Additions Report",
					"onboard": 1,
                    "label":_("Item Additions Report")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Edited Items Report",
					"doctype": "Item",
					"onboard": 1,
					"route":"List/Item/Report/Edited Items Report",
                    "label":_("Edited Items Report")
                    
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Recieved Items",
					"doctype": "Item",
					"onboard": 1,
					"dependencies": ["Item"],
                    "label":_("Recieved Items Report")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Movement Report",
					"doctype": "Item",
					"onboard": 1,
					"dependencies": ["Item"],
                     "label":_("Movement Report")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ageing",
					"onboard": 1,
					"doctype": "Item",
					"route":"#List/Item/Report/Disabled Items",
					"dependencies": ["Item"],
                     "label":_("Disabled Item Report")
				},
				# {
				# 	"type": "report",
				# 	"is_query_report": True,
				# 	"name": "Item Price Stock",
				# 	"doctype": "Item",
				# 	"dependencies": ["Item"],
				# 	"route":"#List/Item/Report/Disposed Items",
                #      "label":_("Disposed Items Report"),
				# },
                {
					"type": "report",
					"is_query_report": True,
					"name": "Physical Count Reconciliation Report",
					"onboard": 1,
					"doctype": "Item",
					"dependencies": ["Item"],
					"breadcrumbs" : "Senergy",
					# "route":"#List/Stock Reconciliation/Report/Physical Count Reconciliation ",
                    "label":_("Physical Count Reconciliation Report")
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "Item Card",
					"onboard": 1,
					"doctype": "Item",
					"route":"#List/Item/Report/Item Card",
					"dependencies": ["Item"],
                    "label":_("Item Card")
				}
			]
		},
        {
			"label": _("Analysis Report"),
			"items": [
				# {
				# 	"type": "doctype",
				# 	"name": "Item",
				# 	"route": "#stock-balance",
				# 	"onboard": 1,
                #     "label":_("Stock Summary"),
				# },
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ageing Report",
					"doctype": "Item",
					"onboard": 1,
                    "label":_("Stock Ageing"),
					"dependencies": ["Item"],
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "Slow Moving Report",
					"doctype": "Stock Ledger Entry",
					"onboard": 1,
                    "label":_("Slow Moving"),
					"dependencies": ["Item"],
				},
                {
					"type": "report",
					"is_query_report": True,
					"onboard": 1,
					"name": "Item Price Stock",
                    "label":_("Pricing Analysis"),
					"dependencies": ["Item"],
				}
			]
		},
        {
			"label": _("Management Report"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Inventory Listing",
					"doctype": "Stock Ledger Entry",
					"onboard": 1,
                    "label":_("Inventory Listing"),
					"dependencies": ["Item"],
				},
                {
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ledger",
					"doctype": "Stock Ledger Entry",
					"onboard": 1,
                    "label":_("My Dashboard"),
                    "route": "#dashboard/Inventory",
					"dependencies": ["Item"],
				}
			]
		},
		{
			"label": _("Purchase Reports"),
			"icon": "fa fa-table",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Purchase Analytics",
					"reference_doctype": "Purchase Order",
					"onboard": 1
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Supplier-Wise Sales Analytics",
					"reference_doctype": "Stock Ledger Entry",
					"onboard": 1
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Purchase Order Trends",
					"reference_doctype": "Purchase Order",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Procurement Tracker",
					"reference_doctype": "Purchase Order",
					"onboard": 1,
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Requested Items To Be Ordered",
					"reference_doctype": "Material Request",
					"onboard": 1,
				},
			]
		},
       
     ]
