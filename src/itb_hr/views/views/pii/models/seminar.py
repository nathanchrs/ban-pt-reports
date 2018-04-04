from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class Seminar(models.Model):
    _name = 'pii.seminar'

    name = fields.Char(required=True,index=True,string='Seminar')
    partner_id = fields.Many2one('res.partner',string='Anggota')
    date = fields.Date(string='Tanggal')
    organizer = fields.Char(string='Penyelenggara')
    note = fields.Text(string='Uraian')