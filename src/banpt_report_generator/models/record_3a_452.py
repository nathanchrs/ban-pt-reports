# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_452(models.Model):
    _name = 'banpt_report_generator.record_3a_452'
    _rec_name = 'nama_dosen'
    _title = '3A-4.5.2 Peningkatan Kemampuan Dosen Tetap Melalui Tugas Belajar'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    jenjang_pendidikan = fields.Char(string='Jenjang Pendidikan Lanjut')
    bidang_studi = fields.Char(string='Bidang Studi')
    perguruan_tinggi = fields.Char(string='Perguruan Tinggi')
    negara = fields.Char(string='Negara')
    tahun_pelaksanaan = fields.Char(string='Tahun Pelaksanaan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
