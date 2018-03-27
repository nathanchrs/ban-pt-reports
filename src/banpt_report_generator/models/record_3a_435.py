# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_435(models.Model):
    _name = 'banpt_report_generator.record_3a_435'
    _rec_name = 'nama_dosen'
    _title = '3A-4.3.5 Aktivitas Mengajar Dosen Tetap yang Bidang Keahliannya Di Luar PS'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    kode_matkul = fields.Char(string='Kode Mata Kuliah')
    nama_matkul = fields.Char(string='Nama Mata Kuliah')
    jumlah_sks_matkul = fields.Integer(string='Jumlah SKS')
    jumlah_pertemuan_terencana_matkul = fields.Integer(string='Jumlah Pertemuan : Direncanakan')
    jumlah_pertemuan_terlaksana_matkul = fields.Integer(string='Jumlah Pertemuan : Dilaksanakan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
