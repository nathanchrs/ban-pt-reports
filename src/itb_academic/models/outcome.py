from odoo import models, fields, api, exceptions


class Outcome(models.Model):
    _name = 'itb.academic_outcome'
    
    name = fields.Char(index=True,required=True)
    code = fields.Char(index=True,required=True)
    note = fields.Text()
    active = fields.Boolean(default=True)
    program_ids = fields.Many2many('itb.academic_program',relation='itb_academic_program_outcome_rel',string='Programs')
    catalog_outcome_ids = fields.One2many('itb.academic_catalog_outcome','outcome_id',string='Outcomes')
