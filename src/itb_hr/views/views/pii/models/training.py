from odoo import models, fields, api, exceptions

class Training(models.Model):
	_name = 'pii.training'

	name = fields.Char(string='Pelatihan')
	date = fields.Date(string='Tanggal')
	provider = fields.Char(string='Lembaga')
	credit = fields.Float(string='Jumlah Jam')
	note = fields.Text(string='Uraian')
	partner_id =  fields.Many2one('res.partner', string='Anggota')