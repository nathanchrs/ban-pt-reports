# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_A3_1_4(models.Model):
    _name = 'banpt_report_generator.A3_1_4'
    _rec_name = 'nama'
    _title = 'A3_1_4'

    tahun_masuk = fields.Char(string='Tahun Masuk')
    #jumlah mahasiswa reguler per angkatan pada tahun (tidak termasuk mahasiswa transfer)
    ts6 = fields.Integer(string='TS-6')
    ts5 = fields.Integer(string='TS-5')
    ts4 = fields.Integer(string='TS-4')
    ts3 = fields.Integer(string='TS-3')
    ts2 = fields.Integer(string='TS-2')
    ts1 = fields.Integer(string='TS-1')
    ts = fields.Integer(string='TS')
    lulusan_reguler_sampai_ts = fields.Integer(string='Lulusan s.d. TS (dari Mahasiswa Reguler)')
    tahun_referensi = fields.Integer(string='Tahun Referensi (TS)')


    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
