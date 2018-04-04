from datetime import datetime
from odoo import models, fields, api, exceptions

class Teaching(models.Model):
	_name = 'pii.teaching'

	university = fields.Char(string='Perguruan Tinggi')
	date = fields.Date(string='Tanggal')
	credit = fields.Float(string='SKS')
	courses = fields.Char(string='Mata Kuliah')
	partner_id =  fields.Many2one('res.partner', string='Anggota')