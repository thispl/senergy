# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import today
from frappe.model.document import Document
from erpnext.assets.doctype.asset.depreciation \
	import get_disposal_account_and_cost_center, get_depreciation_accounts

class AssetDisposal(Document):
	def validate(self):
		if(self.workflow_state == "Approved"):
			self.date = today()
			frappe.db.commit()

@frappe.whitelist()
def make_sales_invoice(name):
	asset_disposal = frappe.get_doc("Asset Disposal",name)
	si = frappe.new_doc("Sales Invoice")
	si.company = asset_disposal.company
	si.currency = frappe.get_cached_value('Company',  asset_disposal.company,  "default_currency")
	disposal_account, depreciation_cost_center = get_disposal_account_and_cost_center(asset_disposal.company)
	for asset in asset_disposal.table_10:
		item = frappe.get_doc("Item",asset.item_code)
		si.append("items", {
			"item_code": item.name,
			"item_name": item.item_name,
			"description": item.description,
			"is_fixed_asset": 1,
			"asset": asset.asset,
			"income_account": disposal_account,
			"uom": "Nos",
			"rate":asset.nbv,
			"cost_center": depreciation_cost_center,
			"qty": 1
		})
		si.set_missing_values()
	return si