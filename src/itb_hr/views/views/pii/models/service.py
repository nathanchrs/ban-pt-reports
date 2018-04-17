from datetime import datetime
from odoo import models, fields, api, exceptions

class Service(models.Model):
	_name = 'pii.service'

	organization = fields.Char(string='Organisasi')
	date = fields.Date(string='Tanggal')
	name = fields.Char(string='Posisi')
	note = fields.Text(string='Uraian')
	partner_id =  fields.Many2one('res.partner', string='Anggota')