# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_6111(models.Model):
    _name = 'banpt_report_generator.record_3b_6111'
    _rec_name = 'jenis_dana'
    _title = '3B-6.1.1.1 Jumlah Dana Yang Diterima Fakultas'

    sumber_dana = fields.Text(string='Sumber Dana', required=True)
    jenis_dana = fields.Text(string='Jenis Dana', required=True)
    jumlah_dana_ts_2 = fields.Integer(string='Jumlah Dana TS-2 (juta rupiah)')
    jumlah_dana_ts_1 = fields.Integer(string='Jumlah Dana TS-1 (juta rupiah)')
    jumlah_dana_ts = fields.Integer(string='Jumlah Dana TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clean record_3b_6111 table
        report.record_3b_6111.unlink()
