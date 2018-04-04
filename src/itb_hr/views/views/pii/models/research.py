from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class res(models.Model):
    _name = 'pii.research'

    name = fields.Char(required=True,index=True,string='Jabatan')
    partner_id = fields.Many2one('res.partner',string='Anggota')
    date = fields.Date(string='Tanggal')
    campus = fields.Char(string='Lembaga')
    note = fields.Text(string='Uraian')