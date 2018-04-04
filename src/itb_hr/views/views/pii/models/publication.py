from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class publication(models.Model):
    _name = 'pii.publication'

    name = fields.Char(required=True,index=True,string='Judul')
    partner_id = fields.Many2one('res.partner',string='Anggota')
    date = fields.Date(string='Tanggal')
    publisher = fields.Char(string='Media Publikasi')
    note = fields.Text(string='Uraian')