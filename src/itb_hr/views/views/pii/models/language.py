from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime


class language(models.Model):
    _name = 'pii.language'

    name = fields.Char(required=True,index=True,string='Bahasa')
    partner_id = fields.Many2one('res.partner',string='Anggota')
    reading = fields.Selection([('cukup','Cukup'),('baik','Baik'),('fasih','Fasih')],default='baik',string='Membaca')
    writing = fields.Selection([('cukup','Cukup'),('baik','Baik'),('fasih','Fasih')],default='baik',string='Menulis')
    speaking = fields.Selection([('cukup','Cukup'),('baik','Baik'),('fasih','Fasih')],default='baik',string='Berbicara')
    listening = fields.Selection([('cukup','Cukup'),('baik','Baik'),('fasih','Fasih')],default='baik',string='Mendengar')