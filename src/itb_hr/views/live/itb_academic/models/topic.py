from odoo import models, fields, api, exceptions
   

class Topic(models.Model):
    _name = 'itb.academic_topic'
    
    name = fields.Char(index=True,required=True)
    note = fields.Text()
    sequence = fields.Integer()    
    catalog_id = fields.Many2one('itb.academic_catalog',string='Catalog')
