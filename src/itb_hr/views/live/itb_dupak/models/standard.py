from odoo import models, fields, api, exceptions


class Standard(models.Model):
    _name = 'itb.dupak_standard'

    name = fields.Char(required=True,index=True)
    code = fields.Char(required=True,index=True)
    unit = fields.Char()
    score = fields.Float()
    category = fields.Char()
    note = fields.Text()
    version = fields.Integer()
    active = fields.Boolean()