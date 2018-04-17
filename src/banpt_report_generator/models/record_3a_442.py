# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_442(models.Model):
    _name = 'banpt_report_generator.record_3a_442'
    _rec_name = 'nama_dosen'
    _title = '3A-4.4.2 Aktivitas Mengajar Data Dosen Tidak Tetap'

    nama_dosen = fields.Char(string='Nama Dosen Tidak Tetap', required=True)
    kode_matkul = fields.Char(string='Kode Mata Kuliah')
    nama_matkul = fields.Char(string='Nama Mata Kuliah')
    jumlah_sks_matkul = fields.Integer(string='Jumlah SKS')
    jumlah_pertemuan_terencana_matkul = fields.Integer(string='Jumlah Pertemuan Direncanakan')
    jumlah_pertemuan_terlaksana_matkul = fields.Integer(string='Jumlah Pertemuan Dilaksanakan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_442 table
        report.record_3a_442.unlink()

        # Add aktivitas mengajar dosen tidak tetap
