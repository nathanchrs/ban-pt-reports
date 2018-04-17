from odoo import models, fields, api, exceptions
from datetime import datetime

class Allocation(models.Model):
	_name = 'itb.plan_allocation'
	
	spending_id = fields.Many2one('itb.plan_spending', ondelete='cascade', required=True, index=True)
	spending_id_int = fields.Many2one('itb.plan_spending_int', ondelete='cascade', required=True, index=True)
	budget = fields.Float(default=0, string='Budget')
	date_created = fields.Datetime(string='Date Created', default=datetime.now())
	date_request = fields.Datetime(string='Date Request', default=datetime.now())
	note = fields.Text(string='Note')