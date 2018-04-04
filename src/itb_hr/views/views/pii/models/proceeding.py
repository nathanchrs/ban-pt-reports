from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class proceeding(models.Model):
    _name = 'pii.proceeding'

    name = fields.Char(required=True,index=True,string='Judul')
    partner_id = fields.Many2one('res.partner',string='Anggota')
    date = fields.Date(string='Tanggal')
    conference = fields.Char(string='Seminar/Lokakarya')
    organizer = fields.Char(string='Penyelenggara')
    note = fields.Text(string='Uraian')