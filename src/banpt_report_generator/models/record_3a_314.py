# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_314(models.Model):
    _name = 'banpt_report_generator.record_3a_314'
    _rec_name = 'tahun_masuk'
    _title = '3A-3.1.4 Jumlah Mahasiswa Reguler 7 Tahun Terakhir'

    tahun_masuk = fields.Char(string='Tahun Masuk', required=True)
    ts6 = fields.Integer(string='TS-6')
    ts5 = fields.Integer(string='TS-5')
    ts4 = fields.Integer(string='TS-4')
    ts3 = fields.Integer(string='TS-3')
    ts2 = fields.Integer(string='TS-2')
    ts1 = fields.Integer(string='TS-1')
    ts = fields.Integer(string='TS')
    lulusan_reguler_sampai_ts = fields.Integer(string='Lulusan Reguler s.d. TS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
