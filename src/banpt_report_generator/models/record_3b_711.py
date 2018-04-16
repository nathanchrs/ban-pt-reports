# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_711(models.Model):
    _name = 'banpt_report_generator.record_3b_711'
    _rec_name = 'program_studi'
    _title = '3B-7.1.1 Penelitian'

    program_studi = fields.Text(string='Nama Program Studi', required=True)
    jumlah_judul_penelitian_ts_2 = fields.Text(string='Jumlah Judul Penelitian TS-2', required=True)
    jumlah_judul_penelitian_ts_1 = fields.Text(string='Jumlah Judul Penelitian TS-1', required=True)
    jumlah_judul_penelitian_ts = fields.Text(string='Jumlah Judul Penelitian TS', required=True)
    total_dana_penelitian_ts_2 = fields.Integer(string='Total Dana Penelitian TS-2 (juta rupiah)')
    total_dana_penelitian_ts_1 = fields.Integer(string='Total Dana Penelitian TS-1 (juta rupiah)')
    total_dana_penelitian_ts = fields.Integer(string='Total Dana Penelitian TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
    