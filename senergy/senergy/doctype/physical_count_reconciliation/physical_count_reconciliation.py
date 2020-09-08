# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PhysicalCountReconciliation(Document):
	def on_submit(self):
		for t in self.table_6:
			if int(t.store_quantity) != int(t.physical_quantity):
				doc = frappe.new_doc("Stock Reconciliation")
				doc.purpose = "Stock Reconciliation"
				doc.append("items",{
					"item_code" : t.item,
					"warehouse" : t.warehouse,
					"qty" : t.physical_quantity
				})
				doc.save(ignore_permissions=True)
				doc.submit()
				# frappe.errprint(t.item)

@frappe.whitelist()
def update_wfs(name):
	doc = frappe.get_doc("Physical Count Reconciliation",name)
	if doc.warehouse:
		if "Main" in doc.warehouse:
			frappe.db.set_value("Physical Count Reconciliation",doc.name,"workflow_state","Approval Pending")