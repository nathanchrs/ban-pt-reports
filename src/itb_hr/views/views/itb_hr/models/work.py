from datetime import datetime
from odoo import models, fields, api, exceptions

class Work(models.Model):
	_name = 'itb.hr_work'

	def _set_current_employee(self):
		return self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
	
	name = fields.Char(string="Last Position")
	company = fields.Char()
	company_scope = fields.Selection([('local','Local'),('national','National'),('global','Global')],default="national")
	city = fields.Char()
	reference = fields.Char()
	decision = fields.Date()
	signed_by = fields.Char()
	start = fields.Date()
	finish = fields.Date()
	#duration = fields.Integer(compute='_set_duration',readonly=True)
	duration = fields.Integer()
	state = fields.Selection([('draft','Draft'),('valid','Validated')], 'Status', default='draft', required=True, readonly=True, copy=False)
	employee_id =  fields.Many2one('hr.employee', string='Name', default=_set_current_employee)
	country_id =  fields.Many2one('res.country', string='Country', default='Indonesia')
	research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)

	#@api.one
	#@api.constrains('start','finish')
	def _start_date_no_more_then_finish_date(self):
		if self.start > self.finish:
			raise exceptions.ValidationError('finish date should be greather equal then start date')

	def _set_duration(self):
		start_converted = self.start.year
		finish_converted = self.finish.year
		self.duration = finish_converted - start_converted

	@api.multi
	def action_state_draft(self):
		self.state = 'draft'

	@api.multi
	def action_state_confirm(self):
		self.state = 'confirmed'

	@api.multi
	def action_state_valid(self):
		self.state = 'valid'