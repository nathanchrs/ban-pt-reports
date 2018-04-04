from odoo import models, fields, api, exceptions

class Membership(models.Model):
	_name = 'pii.membership'

	name = fields.Char(string='Organisasi')
	role = fields.Char(string='Posisi')
	note = fields.Text(string='Tugas')
	start = fields.Date(string='Mulai')
	finish = fields.Date(string='Akhir')
	partner_id =  fields.Many2one('res.partner', string='Anggota')