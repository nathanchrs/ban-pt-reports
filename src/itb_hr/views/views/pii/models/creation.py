from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class creation(models.Model):
    _name = 'pii.creation'

    name = fields.Char(required=True,index=True,string='Karya')
    partner_id = fields.Many2one('res.partner',string='Anggota')
    year = fields.Integer(string='Tahun')
    note = fields.Text(string='Uraian')
    publisher = fields.Char(string='Media Publikasi')