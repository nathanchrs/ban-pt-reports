from odoo import models, fields, api, exceptions

class Ado_Itb(models.Model):
    _name = 'itb.plan_ado'
    _rec_name = 'code'
    code = fields.Selection(([('om','ADO_OM'),('pppk', 'ADO_PPPK'),('pnlt','ADO_PNLT')]))
    year = fields.Integer()
    #pagu_id = fields.Many2one('itb.plan_pagu', index=True)
    #pagu_id = fields.Many2one('itb.plan_pagu',ondelete='cascade',required=True,index=True)
    subactivity_id = fields.Many2one('itb.plan_subactivity')