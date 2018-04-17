from odoo import models, fields, api, exceptions

class Pagu(models.Model):
	_name = 'itb.plan_pagu'
	_rec_name = 'unit_id'

	#ado_ids = fields.One2many('itb.plan_ado', 'pagu_id', string='Ado')
	#ado_ids = fields.One2many('itb.plan_ado', 'pagu_id', 'Ado', copy=True)
	code = fields.Selection(([('om','ADO_OM'),('pppk', 'ADO_PPPK'),('pnlt','ADO_PNLT')]))
	unit_id = fields.Many2one('itb.plan_unit',ondelete='cascade',required=True,index=True)
	budget = fields.Float()
	year = fields.Integer()