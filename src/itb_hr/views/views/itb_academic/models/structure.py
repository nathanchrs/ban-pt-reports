from odoo import models, fields, api, exceptions

class Structure(models.Model):
    _name = 'itb.academic_structure'
    
    name = fields.Char()
    parent_id = fields.Many2one('itb.academic_structure',index=True,ondelete='restrict',string='Parent Structure')
    child_ids = fields.One2many('itb.academic_structure','parent_id',string='Child Structure')