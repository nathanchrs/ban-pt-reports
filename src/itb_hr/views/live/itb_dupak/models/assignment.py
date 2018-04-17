from odoo import models, fields, api, exceptions

class Assignment(models.Model):
    _inherit = 'itb.hr_assignment'
    
    standard_id =  fields.Many2one('itb.dupak_standard',string='DUPAK Standard',domain="[('category','like','assignment')]")
	