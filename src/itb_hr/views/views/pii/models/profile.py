from odoo import models, fields, api, exceptions

class Profil(models.Model):
	_inherit = 'res.partner'
	
	religion = fields.Selection([('islam','Islam'),('kristen','Kristen'),('buddha','Buddha'),('hindu','Hindu')],default='islam',string='Agama')
	marital_status = fields.Selection([('lajang','Lajang'),('menikah','Menikah')],default='menikah',string='Pernikahan')
	company_address = fields.Char(string='Alamat Perusahaan')
	education_ids = fields.One2many('pii.education', 'partner_id', string='Pendidikan')
	membership_ids = fields.One2many('pii.membership', 'partner_id', string='Keanggotaan')
	award_ids = fields.One2many('pii.award', 'partner_id', string='Penghargaan')
	training_ids = fields.One2many('pii.training', 'partner_id', string='Pelatihan')
	work_ids = fields.One2many('pii.work', 'partner_id', string='Pekerjaan')
	teaching_ids = fields.One2many('pii.teaching', 'partner_id', string='Pengajaran')
	service_ids = fields.One2many('pii.service', 'partner_id', string='Pengabdian')
	creation_ids = fields.One2many('pii.creation', 'partner_id', string='Karya')
	language_ids = fields.One2many('pii.language', 'partner_id', string='Bahasa')
	proceeding_ids = fields.One2many('pii.proceeding', 'partner_id', string='Makalah')
	publication_ids = fields.One2many('pii.publication', 'partner_id', string='Karya Ilmiah')
	research_ids = fields.One2many('pii.research', 'partner_id', string='Penelitian')
	seminar_ids = fields.One2many('pii.seminar', 'partner_id', string='Seminar')
