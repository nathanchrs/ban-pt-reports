from odoo import models, fields, api, exceptions

class Jabatan(models.Model):
	_name = 'itb.hr_jabatan'
	_rec_name = 'jabatan'
	
	jabatan = fields.Char()
	reference = fields.Char()
	credit = fields.Float()
	major = fields.Char()
	decision = fields.Date()
	signed_by = fields.Char()
	start = fields.Date()
	finish = fields.Date()
	jabatan_id =  fields.Many2one('itb.hr_jabatan_type')
	employee_id =  fields.Many2one('hr.employee', string='Name')
	research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)

	
class Jabatan_Type(models.Model):
	_name = 'itb.hr_jabatan_type'
	
	name = fields.Char()
	sequence = fields.Integer()