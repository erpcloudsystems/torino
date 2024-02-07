# Copyright (c) 2024, ECS and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class GroupCashEntry(Document):
# 	pass

import frappe
from frappe.model.document import Document

class GroupCashEntry(Document):
	@frappe.whitelist()
	def validate(self):
		self.total_amount = 0
		for x in self.expense_entry_account:
			self.total_amount += x.amount

	@frappe.whitelist()
	def before_submit(self):
		for account in self.expense_entry_account:
			cash_entry = frappe.new_doc('Cash Entry')
			cash_entry.company = self.company
			cash_entry.payment_type = self.payment_type
			cash_entry.amount = self.amount
			cash_entry.mode_of_payment = self.mode_of_payment
			cash_entry.account_paid_from = self.account_paid_from
			cash_entry.account_paid_to = self.account_paid_to
			cash_entry.total_amount = self.total_amount
			cash_entry.append('expense_entry_account', 
				{
					"account": account.account,
					"is_credit": account.is_credit,
					"party_type": account.party_type,
					"party": account.party,
					"cost_center": account.cost_center,
					"amount": account.amount,
					"user_remark": account.user_remark,
					"vehicle": account.vehicle,
					"branch": account.branch,
					"project": account.project,
					"نوع_المصروف": account.نوع_المصروف

				}
			)
			cash_entry.remarks = self.remarks
			cash_entry.posting_date = self.posting_date
			cash_entry.group_cash_entry = self.name
			cash_entry.insert(ignore_permissions=True)
			cash_entry.submit()
		pass
	pass


