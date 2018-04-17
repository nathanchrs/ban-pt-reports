# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_321(models.Model):
    _name = 'banpt_report_generator.record_3b_321'
    _rec_name = 'program_studi'
    _title = '3B-3.2.1 Mahasiswa dan Lulusan'

    program_studi = fields.Char(string='Program Studi', required=True)
    rata_masa_studi_1 = fields.Float(string='Rata-rata Masa Studi Tahun 1')
    rata_masa_studi_2 = fields.Float(string='Rata-rata Masa Studi Tahun 2')
    rata_masa_studi_3 = fields.Float(string='Rata-rata Masa Studi Tahun 3')
    rata_ipk_lulusan_1 = fields.Float(string='Rata-rata IPK Lulusan 1')
    rata_ipk_lulusan_2 = fields.Float(string='Rata-rata IPK Lulusan 1')
    rata_ipk_lulusan_3 = fields.Float(string='Rata-rata IPK Lulusan 1')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
