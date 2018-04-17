from odoo import models, fields, api, exceptions


class Price(models.Model):
	_name = 'itb.plan_price'
	
	name = fields.Char()
	code = fields.Char()
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type', default='barang')
	standard = fields.Char()
	amount = fields.Float()
	note = fields.Text()
	centralized = fields.Boolean()
	subactivity_id = fields.Many2one('itb.plan_subactivity')
