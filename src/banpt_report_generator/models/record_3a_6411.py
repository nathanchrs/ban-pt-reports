# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_6411(models.Model):
    _name = 'banpt_report_generator.record_3a_6411'
    _rec_name = 'jenis_pustaka'
    _title = '3A-6.4.1.1 Pustaka'

    jenis_pustaka = fields.Text(string='Jenis Pustaka')
    jumlah_judul = fields.Integer(string='Jumlah Judul')
    jumlah_copy = fields.Integer(string='Jumlah Copy')
    
    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
