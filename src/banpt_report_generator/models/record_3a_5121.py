# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_5121(models.Model):
    _name = 'banpt_report_generator.record_3a_5121'
    _rec_name = 'jenis_mata_kuliah'
    _title = '3A-5.1.2.1 Jumlah SKS Mata Kuliah Wajib dan Pilihan'

    jenis_mata_kuliah = fields.Text(string='Jenis Mata Kuliah', required=True)
    sks = fields.Integer(string='SKS')
    keterangan = fields.Text(string='Keterangan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_5121 table
        report.record_3a_5121.unlink()

        # Add record_3a_5121 according to program_id
