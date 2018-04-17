from odoo import models, fields, api, exceptions

class Plan_Program(models.Model):
	_name = 'itb.plan_program'
	
	name = fields.Char()
	code = fields.Char()
	
	
class Activity(models.Model):
	_name = 'itb.plan_activity'
	
	name = fields.Char()
	code = fields.Char()
	program_id = fields.Many2one('itb.plan_program',ondelete='cascade',required=True,index=True)
	
	
	
class Subactivity(models.Model):
	_name = 'itb.plan_subactivity'
	
	name = fields.Char()
	code = fields.Char()
	activity_id = fields.Many2one('itb.plan_activity',ondelete='cascade',required=True,index=True)
