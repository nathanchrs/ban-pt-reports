# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_622(models.Model):
    _name = 'banpt_report_generator.record_3a_622'
    _rec_name = 'tahun'
    _title = '3A-6.2.2 Dana Untuk Kegiatan Penelitian'

    tahun = fields.Char(string='Tahun', required=True)
    judul_penelitian = fields.Text(string='Judul Penelitian')
    sumber_jenis_dana = fields.Text(string='Sumber dan Jenis Dana')
    jumlah_dana = fields.Integer(string='Jumlah Dana (dalam juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
