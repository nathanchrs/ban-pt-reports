from odoo import models, fields, api, exceptions

class Award(models.Model):
	_name = 'pii.award'
	
	name = fields.Char(string='Penghargaan')
	endorser = fields.Char(string='Lembaga')
	date = fields.Date(string='Tanggal')
	partner_id =  fields.Many2one('res.partner', string='Anggota')