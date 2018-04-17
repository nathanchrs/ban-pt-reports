from odoo import models, fields, api, exceptions

class Ado_Itb(models.Model):
	_name = 'itb.plan_ado'
	_rec_name = 'code'
	code = fields.Selection(([('om','ADO_OM'),('pppk', 'ADO_PPPK'),('pnlt','ADO_PNLT')]))
	year = fields.Integer()
	subactivity_id = fields.Many2one('itb.plan_subactivity')