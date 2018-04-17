from odoo import models, fields, api, exceptions

class Education(models.Model):
	_name = 'pii.education'
	
	name = fields.Char(string='Universitas')
	major = fields.Char(string='Jurusan')
	degree = fields.Selection([('diploma','Diploma'),('sarjana','Sarjana'),('master','Master'),('doktor','Doktor'),('post-doc','Post Doktoral')],default="sarjana",string='Jenjang')
	finish = fields.Date(string='Tanggal Lulus')
	thesis = fields.Text(string='Skripsi')
	city = fields.Char(string='Kota')
	ipk = fields.Float(string='IPK')
	partner_id =  fields.Many2one('res.partner', string='Anggota')
	country_id =  fields.Many2one('res.country', string='Negara', default='ID')