from odoo import api, fields, models


class evaluation(models.Model):
    _name = 'qms.evaluation'

    partner_id = fields.Many2one('res.partner',string='Vendor')
    year = fields.Integer()
    safety = fields.Float()
    quality = fields.Float()
    delivery = fields.Float()
    price = fields.Float()
    quantity = fields.Float()
    document = fields.Float()
    response = fields.Float()
    score = fields.Float()
    grade = fields.Selection([('A','A'),('B','B'),('C','C'),('D','D'),('E','E')])
    keep = fields.Boolean()