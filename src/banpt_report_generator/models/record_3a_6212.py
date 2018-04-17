# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_6212(models.Model):
    _name = 'banpt_report_generator.record_3a_6212'
    _rec_name = 'jenis_penggunaan'
    _title = '3A-6.2.1.2 Penggunaan Dana Perolehan dan Alokasi Dana'

    jenis_penggunaan = fields.Text(string='Jenis Penggunaan', required=True)
    penggunaan_ts_2 = fields.Integer(string='Penggunaan TS-2 (juta rupiah)')
    penggunaan_ts_1 = fields.Integer(string='Penggunaan TS-1 (juta rupiah)')
    penggunaan_ts = fields.Integer(string='Penggunaan TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
