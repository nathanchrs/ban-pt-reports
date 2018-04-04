from odoo import models, fields, api, exceptions
from datetime import datetime

class Family(models.Model):
	_name = 'itb.hr_family'

	def _set_current_employee(self):
		return self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
	
	name = fields.Char()
	relation = fields.Selection([('spouse','Spouse'),('child','Child')],default="spouse")
	relation_reference = fields.Char()
	is_insured = fields.Boolean()
	sex = fields.Selection([('Laki-Laki','Laki-Laki'),('Perempuan','Perempuan')])
	birthdate = fields.Date()
	marital_date = fields.Date()
	marital_status = fields.Char()
	marital_reference = fields.Char()
	birthplace = fields.Char()
	is_inherit = fields.Boolean()
	address =  fields.Char()
	zip = fields.Char()
	age = fields.Integer(compute='_set_age',store=True)
	note = fields.Char()
	state = fields.Selection([('draft','Draft'),('valid','Validated')], 'Status', default='draft',required=True, readonly=True, copy=False)
	employee_id =  fields.Many2one('hr.employee', string='Employee Name', default=_set_current_employee)
	research_group_id = fields.Many2one('itb.hr_research_group', related='employee_id.research_group_id', string="Research Group", readonly=True, store=True)
	
	#@api.constrains('birthdate')
	def _birthdate_not_beyond_today(self):
		format = '%Y-%m-%d %H:%M:%S'
		format_date = '%Y-%m-%d'
		converted_birthdate_year = datetime.strptime(self.birthdate,format_date).date()
		converted_today = datetime.strptime(fields.Datetime.now(),format).date()
		if converted_birthdate_year > converted_today:
			raise exceptions.ValidationError('Birthdate must not exceed todays date!')

	@api.multi
	@api.depends('birthdate')
	def _set_age(self):
		#self.ensure_one()
		
		for family in self:
			family.age = 0
			if family.birthdate != False:
				format = '%Y-%m-%d %H:%M:%S'
				format_date = '%Y-%m-%d'
				converted_birthdate_year = datetime.strptime(family.birthdate,format_date).year
				converted_today_year = datetime.strptime(fields.Datetime.now(),format).date().year
				if (converted_today_year - converted_birthdate_year) > 0:
					family.age = converted_today_year - converted_birthdate_year

	@api.multi
	def action_state_draft(self):
		self.state = 'draft'

	@api.multi
	def action_state_confirm(self):
		self.state = 'confirmed'

	@api.multi
	def action_state_valid(self):
		self.state = 'valid'