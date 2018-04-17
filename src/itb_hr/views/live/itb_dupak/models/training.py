from odoo import models, fields, api, exceptions

class Training(models.Model):
    _inherit = 'itb.hr_training'
    
    standard_id =  fields.Many2one('itb.dupak_standard',string='DUPAK Standard',domain="[('category','like','training')]")
	