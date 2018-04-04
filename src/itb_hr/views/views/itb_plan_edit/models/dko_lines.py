from odoo import models, fields, api, exceptions
from odoo.osv import osv
from datetime import date
from datetime import timedelta

class Dko_Allocation(models.Model):
	_name = 'itb.plan_dko_allocation'
	
	dko_alo_id = fields.Many2one('itb.plan_dko',ondelete='cascade',required=True,index=True)
	dko_spen_id = fields.Many2one('itb.plan_spending_int',ondelete='cascade',required=True,index=True)
	initiative = fields.Char(related='dko_spen_id.plan_line_id.name', readonly=True, store=True)
	unit_id = fields.Many2one(related='dko_spen_id.unit_id', readonly=True, store=True)
	used = fields.Float(default=0, related='dko_spen_id.used', readonly=True, store=True)
	available = fields.Float(default=0, related='dko_spen_id.available', readonly=True,store=True)
	month=fields.Selection(related='dko_spen_id.month', readonly=True, store=True)
	program_id = fields.Many2one(related='dko_spen_id.plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one(related='dko_spen_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one(related='dko_spen_id.plan_line_id.subactivity_id', readonly=True, store=True)
	total_alo = fields.Float(default=0)

class Dko_Taken(models.Model):
	_name = 'itb.plan_dko_taken'
	
	dko_taken_id = fields.Many2one('itb.plan_dko',ondelete='cascade',required=True,index=True)
	actual_id = fields.Many2one('itb.plan_spending_actual',ondelete='cascade',required=True,index=True)
	initiative = fields.Char(related='actual_id.plan_line_id.name', readonly=True, store=True)
	unit_id = fields.Many2one(related='actual_id.unit_id', readonly=True, store=True)
	used = fields.Float(default=0, related='actual_id.used', readonly=True, store=True)
	avai_taken = fields.Float(default=0, related='actual_id.available', readonly=True, store=True)
	month=fields.Selection(related='actual_id.month', readonly=True, store=True)
	program_id = fields.Many2one(related='actual_id.spending_id.plan_line_id.program_id', readonly=True, store=True)
	activity_id = fields.Many2one(related='actual_id.spending_id.plan_line_id.activity_id', readonly=True, store=True)
	subactivity_id = fields.Many2one(related='actual_id.spending_id.plan_line_id.subactivity_id', readonly=True, store=True)
	tot_taken = fields.Float(default=0)