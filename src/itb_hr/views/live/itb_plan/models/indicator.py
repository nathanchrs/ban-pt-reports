from odoo import models, fields, api, exceptions

class Indicator(models.Model):
	_name = 'itb.plan_indicator'
	
	name = fields.Char()
	code = fields.Char()
	standard = fields.Char()
	is_reinforce = fields.Boolean(default=True)
	activity_id = fields.Many2one('itb.plan_activity')