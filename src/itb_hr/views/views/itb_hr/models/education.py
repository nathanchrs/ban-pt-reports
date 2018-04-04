from odoo import models, fields, api, exceptions

class Education(models.Model):
	_name = 'itb.hr_education'
	#_rec_name = 'school'

	def _set_current_employee(self):
		return self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
	
	name = fields.Char(related='school')
	school = fields.Char()
	major = fields.Char()
	degree = fields.Selection([('kindergarten','Kindergarten'),('elementary','Elementary'),('junior-high','Junior High'),('senior-high','Senior High'),('diploma','Diploma'),('undergraduate','Undergraduate'),('graduate','Graduate'),('doctoral','Doctoral'),('post-doc','Post Doctoral')],default="undergraduate")
	start = fields.Date()
	finish = fields.Date()
	thesis = fields.Char()
	city = fields.Char()
	certificate_signer = fields.Char()
	state = fields.Selection([('draft','Draft'),('valid','Validated')], 'Status', default='draft', required=True, readonly=True, copy=False)
	employee_id =  fields.Many2one('hr.employee', string='Name', default=_set_current_employee)
	country_id =  fields.Many2one('res.country', string='Country', default='Indonesia')
	research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)
	
	@api.multi
	@api.constrains('start','finish')
	def _start_date_no_more_then_finish_date(self):
		self.ensure_one()
		if self.start > self.finish:
			raise exceptions.ValidationError('finish date should be greather equal then start date')

	@api.multi
	def action_state_draft(self):
		self.state = 'draft'

	@api.multi
	def action_state_confirm(self):
		self.state = 'confirmed'

	@api.multi
	def action_state_valid(self):
		self.state = 'valid'