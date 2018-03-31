# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_541(models.Model):
    _name = 'banpt_report_generator.record_3a_541'
    _rec_name = 'nama_dosen'
    _title = '3A-5.4.1 Dosen Pembimbing Akademik dan Jumlah Mahasiswa'

    nama_dosen = fields.Text(string='Nama Dosen Pembimbing Akademik', required=True)
    jumlah_mhs_bimbingan = fields.Integer(string='Jumlah Mahasiswa Bimbingan', required=True)
    rata_banyaknya_mahasiswa_per_smt = fields.Integer(string='Rata-rata Banyaknya Pertemuan Mahasiswa/Semester', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
