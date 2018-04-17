from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime



class committee(models.Model):
    _name = 'qms.committee'

    name = fields.Char(required=True,string='Issue')
    date = fields.Date(required=True)
    capa_ids = fields.One2many('qms.capa','committee_id',string='CAPA')
    participant_ids = fields.Many2many('res.partner',string='Participants', domain="[('role','=','employee')]")
    production_ids = fields.Many2many('qms.production',string='Production')
    products = fields.Char(compute='_get_products',store=True)
    participants = fields.Char(compute='_get_participants',store=True)
    state = fields.Selection([('open','Open'),('close','Close')],default='open')


    @api.depends('participant_ids')
    def _get_participants(self):
        for record in self:
            if record.participant_ids:
                participant_list = [x.name for x in record.participant_ids]
                record.participants = ', '.join(participant_list) 


    def _get_products(self):
        for record in self:
            if record.production_ids:
                product_list = [x.product_id.name for x in record.production_ids]
                record.products = ', '.join(product_list)