from odoo import models, fields, api, exceptions

class Evaluation(models.Model):
	_name = 'itb.plan_evaluation'
	_rec_name = 'plan_id'
	
	percent_performance = fields.Float()
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated')], 'Status', default='draft')
	plan_id = fields.Many2one('itb.plan',ondelete='cascade',required=True,index=True,domain="[('state','=','validate')]")
	evaluation_line_ids = fields.One2many('itb.plan_evaluation_line', 'evaluation_id', 'Plan Evaluation Lines', copy=True)
	
	
class Evaluation_Line(models.Model):
	_name = 'itb.plan_evaluation_line'
	
	initiative = fields.Char(related='target_id.plan_line_id.name')
	plan = fields.Float(related='target_id.plan')
	actual = fields.Float()
	note = fields.Text()
	target_id = fields.Many2one('itb.plan_target',ondelete='cascade',required=True,index=True)
	evaluation_id = fields.Many2one('itb.plan_evaluation',ondelete='cascade',required=True,index=True)