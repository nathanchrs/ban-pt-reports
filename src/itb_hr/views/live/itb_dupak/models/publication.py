from odoo import models, fields, api, exceptions

class Publication(models.Model):
    _inherit = 'itb.hr_publication'
    
    standard_id =  fields.Many2one('itb.dupak_standard',string='DUPAK Standard',domain="[('category','like','publication')]")
	