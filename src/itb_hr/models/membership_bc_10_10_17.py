from odoo import models, fields, api, exceptions

class Membership(models.Model):
	_name = 'itb.hr_membership'

	def _set_current_employee(self):
		return self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
	
	name = fields.Char()
	role = fields.Selection([('member','Member'),('honor','Honorable'),('leader','Leader')])
	level = fields.Selection([('local','Local'),('province','province'),('national','National'),('global','Global')],default="national")
	start = fields.Date()
	finish = fields.Date()
	#state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('valid','Validated')], 'Status', default='draft',required=True, readonly=True, copy=False)
	state = fields.Selection([('draft','Draft'),('valid','Validated')], 'Status', default='draft', copy=False)
	employee_id =  fields.Many2one('hr.employee', string='Employee', default=_set_current_employee)

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
	def action_state_valid(self):
		self.state = 'valid'