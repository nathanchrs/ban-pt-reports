from datetime import datetime
from odoo import models, fields, api, exceptions

class Work(models.Model):
	_name = 'pii.work'

	name = fields.Char(string="Jabatan")
	company = fields.Char(string='Perusahaan')
	start = fields.Date(string='Mulai')
	finish = fields.Date(string='Akhir')
	note = fields.Text(string='Uraian')
	partner_id =  fields.Many2one('res.partner', string='Anggota')
