# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_6112(models.Model):
    _name = 'banpt_report_generator.record_3b_6112'
    _rec_name = 'jenis_penggunaan'
    _title = '3B-6.1.1.2 Penggunaan Dana'

    jenis_penggunaan = fields.Text(string='Jenis Dana', required=True)
    jumlah_dana_ts_2 = fields.Integer(string='Jumlah Dana TS-2 (juta rupiah)')
    jumlah_dana_ts_1 = fields.Integer(string='Jumlah Dana TS-1 (juta rupiah)')
    jumlah_dana_ts = fields.Integer(string='Jumlah Dana TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clean record_3b_6112 table
        report.record_3b_6112.unlink()
