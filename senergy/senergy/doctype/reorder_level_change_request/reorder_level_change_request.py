# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ReorderLevelChangeRequest(Document):
	def on_submit(self):
		item = frappe.get_doc("Item",self.item_code)
		to_remove = [ row for row in item.reorder_levels]
		[ item.remove(row) for row in to_remove ]
		child = self.reorder_item
		for c in child:
			item.append("reorder_levels",{
				"warehouse_reorder_level" : c.change_reorder_level,
				"warehouse_reorder_qty": c.change_reorder_qty,
				"warehouse_group" : c.warehouse_group,
				"warehouse" : c.warehouse,
				"material_request_type" : c.material_request_type
			})
		item.save(ignore_permissions=True)

