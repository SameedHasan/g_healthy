# Copyright (c) 2023, Sameed Hasan and contributors
# For license information, please see license.txt

import re
import frappe
from frappe.model.document import Document

class PageTabs(Document):
	def validate(self):
		if self.parent_doctype and self.page:
			if self.parent_doctype == self.page:
				frappe.throw('doctype cannot be same as parent doctype')
		if self.view=='Custom View' and not self.component:
			frappe.throw("Template is required")
		if self.route:
			if frappe.db.exists("Page Tabs", {"route": self.route, "sequence_number": self.sequence_number, "name": ["!=", self.name]}):
				frappe.throw('Sequence already exists for this route')
		if self.menu_item:
			if frappe.db.exists("Page Tabs", {"menu_item": self.menu_item, "sequence_number": self.sequence_number, "name": ["!=", self.name]}):
				frappe.throw('Sequence already exists for this Menu Items')
		if self.parent_doctype and self.heading:
			fields = frappe.get_meta(self.parent_doctype).fields
			regex = re.compile(r'\{([^}]+)\}')
			matches = regex.findall(self.heading)
			flag = 0
			for field_name in matches:
				field_exists = any(field.fieldname == field_name for field in fields)
				if not field_exists:
					flag = 1
			if flag == 1:
				frappe.throw("Heading expression is not valid.")
