# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_623(models.Model):
    _name = 'banpt_report_generator.record_3a_623'
    _rec_name = 'tahun'
    _title = '3A-6.3.1 Dana Pelayanan/Pengabdian Kepada Masyarakat'

    tahun = fields.Char(string='Tahun', required=True)
    judul_kegiatan = fields.Text(string='Judul Kegiatan Pelayanan/Pengabdian kepada Masyarakat')
    sumber_jenis_dana = fields.Text(string='Sumber dan Jenis Dana')
    jumlah_dana = fields.Integer(string='Jumlah Dana (dalan juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
