from odoo import models, fields, api, exceptions

class Award(models.Model):
    _inherit = 'itb.hr_award'
    
    standard_id =  fields.Many2one('itb.dupak_standard',string='DUPAK Standard',domain="[('category','like','award')]")
	