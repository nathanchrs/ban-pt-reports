from odoo import models, fields, api, exceptions

class Pangkat(models.Model):
	_name = 'itb.hr_pangkat'
	_rec_name = 'pangkat'

	pangkat = fields.Char()
	pangkat_id =  fields.Many2one('itb.hr_pangkat_type')
	reference = fields.Char()
	decision = fields.Date()
	signed_by = fields.Char()
	start = fields.Date()
	finish = fields.Date()
	
	employee_id =  fields.Many2one('hr.employee', string='Name')
	research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)

	
class Pangkat_Type(models.Model):
	_name = 'itb.hr_pangkat_type'
	
	name = fields.Char()
	code = fields.Char()
	sequence = fields.Integer()