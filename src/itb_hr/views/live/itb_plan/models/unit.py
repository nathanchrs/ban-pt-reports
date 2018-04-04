from odoo import models, fields, api, exceptions

class Unit(models.Model):
	_name = 'itb.plan_unit'
	
	name = fields.Char()
	user_id = fields.Many2one('res.users')