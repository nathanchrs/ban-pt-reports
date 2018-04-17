from odoo import models, fields, api, exceptions

class Graduation(models.Model):
    _name = 'itb.academic_graduation'
    
    name = fields.Char(index=True)
    amount = fields.Integer(readonly=True)
    author_ids = fields.Many2many('itb.academic_author',relation='itb_academic_graduation_author')