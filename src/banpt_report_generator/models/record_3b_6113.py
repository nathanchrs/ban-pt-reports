# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_6113(models.Model):
    _name = 'banpt_report_generator.record_3b_6113'
    _rec_name = 'nama_prodi'
    _title = '3B-6.1.1.3 Penggunaan Dana Untuk Tridarma'

    nama_prodi = fields.Text(string='Jenis Dana', required=True)
    jumlah_dana_ts_2 = fields.Integer(string='Jumlah Dana TS-2 (juta rupiah)')
    jumlah_dana_ts_1 = fields.Integer(string='Jumlah Dana TS-1 (juta rupiah)')
    jumlah_dana_ts = fields.Integer(string='Jumlah Dana TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
