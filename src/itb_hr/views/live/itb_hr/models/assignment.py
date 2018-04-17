from odoo import models, fields, api, exceptions

class Assignment(models.Model):
	_name = 'itb.hr_assignment'
	_rec_name = 'job_id'
	
	reference = fields.Char()
	decision = fields.Date()
	start = fields.Date()
	finish = fields.Date()
	signed_by = fields.Char()
	office = fields.Char()
	
	job_id =  fields.Many2one('hr.job', string='Job Title')
	department_id =  fields.Many2one('hr.department', string='Department')
	employee_id =  fields.Many2one('hr.employee', string='Name')
	research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)