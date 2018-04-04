from odoo import models, fields, api, exceptions


class Target(models.Model):
	_name = 'itb.plan_target'
	
	name = fields.Char(required=True, related='indicator_id.name')
	standard = fields.Char(related='indicator_id.standard')
	plan = fields.Float(required=True)
	actual = fields.Float(default=0, required=True)
	percent_performance = fields.Float(default=0, readonly=True, compute='_compute_percent_performance')
	
	plan_line_id = fields.Many2one('itb.plan_line',domain="[('plan_id','=',plan_id)]",ondelete='cascade',required=True,index=True)
	indicator_id = fields.Many2one('itb.plan_indicator',ondelete='cascade',required=True,index=True)
	plan_id = fields.Many2one(related='plan_line_id.plan_id',store='True',index=True,domain="[('state','=','validate')]")

	@api.one
	@api.constrains('plan')
	def _not_less_zero(self):
		if self.plan <= 0.00:
			raise exceptions.ValidationError("Plan do not less than zero.")
	
	@api.one
	@api.depends('plan_id', 'actual', 'indicator_id')
	def _compute_percent_performance(self):
		if self.actual == 0 or self.plan == 0:
			self.percent_performance = 0
		else:
			if self.indicator_id.is_reinforce:
				self.percent_performance = self.actual / self.plan
			else:
				self.percent_performance = self.plan / self.actual
