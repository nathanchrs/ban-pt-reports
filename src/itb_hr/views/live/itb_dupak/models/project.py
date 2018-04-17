from odoo import models, fields, api, exceptions

class Project(models.Model):
    _inherit = 'itb.hr_project'
    
    standard_id =  fields.Many2one('itb.dupak_standard',string='DUPAK Standard',domain="[('category','like','project')]")
	