from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class assesment(models.Model):
    _name = 'qms.assesment'
    
    name = fields.Char(required=True)
    date = fields.Date(required=True)
    allow_closing = fields.Boolean()
    closing_date = fields.Date()
    state = fields.Selection([('open','Open'),('close','Close')],default='open')
    assesor_ids = fields.Many2many('res.partner',string='Assesor', domain="[('role','=','employee')]")
    capa_ids = fields.One2many('qms.capa','assesment_id',string='CAPA')
    product_ids = fields.Many2many('product.product',domain="[('sale_ok','=',True)]",string='Products')