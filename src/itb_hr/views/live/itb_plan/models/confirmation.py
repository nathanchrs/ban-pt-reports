from odoo import models, fields, api, exceptions
from datetime import date


class Confirmation(models.Model):
	_name = 'itb.plan_confirmation'
	_rec_name = 'plan_id'
	
	reference = fields.Char()
	month = fields.Selection([('Jan','Jan'),('Feb', 'Feb'),('Mar','Mar'),('Apr','Apr'),('May','May'),('Jun','Jun'),('Jul','Jul'),('Aug','Aug'),('Sep','Sep'),('Oct','Oct'),('Nov','Nov'),('Dec','Dec')], 'Month',default='Jan')
	type = fields.Selection([('barang','Barang'),('pegawai', 'Pegawai'),('jasa','Jasa'),('modal','Modal')], 'Type')
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('validate','Validated')], 'Status', default='draft')
	note = fields.Text()
	plan_id = fields.Many2one('itb.plan',ondelete='cascade',required=True,index=True,domain="[('state','=','validate')]")
	program_id = fields.Many2one('itb.plan_program',ondelete='cascade',required=True,index=True)
	confirmation_line_ids = fields.One2many('itb.plan_confirmation_line', 'confirmation_id', 'Confirmation Lines', copy=True)

	def action_budget_conf_state_confirmed(self):
		self.write({ 'state' : 'confirm' })
		return True

	def action_budget_conf_state_validated(self):
		self.write({ 'state' : 'validate' })
		return True

	def action_budget_conf_state_abort(self):
		self.write({ 'state' : 'draft' })
		return True
        
        
class Confirmation_Line(models.Model):
	_name = 'itb.plan_confirmation_line'
	
	spending_actual_id = fields.Many2one('itb.plan_spending_actual',ondelete='cascade',required=True,index=True)
	confirmation_id = fields.Many2one('itb.plan_confirmation',ondelete='cascade',required=True,index=True)
	initiative = fields.Char(related='spending_actual_id.plan_line_id.name')
	type = fields.Selection(related='spending_actual_id.type')
	month = fields.Selection(related='spending_actual_id.month')
	total = fields.Float(related='spending_actual_id.total')
