from odoo import models, fields, api, exceptions


class Budget_Manager_Wizard(models.TransientModel):
	_name = 'itb.plan_budget_manager_wizard'
	
	user_ids = fields.Many2many('res.users',required=True,string='Budget Manager')
	
	@api.multi
	def set_budget_manager(self):
		if not(self.user_ids):
			raise exceptions.ValidationError('No Budget Manager selected!')
		
		ids = self.env.context.get('active_ids',[])
		spendings = self.env['itb.plan_spending_actual'].search([('id','in',ids)])
		for spending in spendings:
			spending.user_ids |= self.user_ids
		
		return{} 		