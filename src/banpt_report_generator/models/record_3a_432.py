# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_432(models.Model):
    _name = 'banpt_report_generator.record_3a_432'
    _rec_name = 'nama'
    _title = '3A-4.3.2 Dosen Tetap yang Bidang Keahliannya Di Luar PS'

    nama = fields.Char(string='Nama Dosen Tetap', required=True)
    nidn = fields.Char(string='NIDN', required=True)
    tanggal_lahir = fields.Date(string='Tanggal lahir')
    jabatan = fields.Selection([('lektor', 'Lektor'), ('lektor_kepala', 'Lektor Kepala'), ('asisten_ahli', 'Asisten Ahli'), ('guru_besar', 'Guru Besar')], string='Jabatan Akademik')
    sertifikasi = fields.Selection([('ya', 'Ya'), ('tidak', 'Tidak')], string='Sertifikasi (Ya/Tidak)')
    asal_pt_s1 = fields.Char(string='Asal PT S1')
    bidang_keahlian_s1 = fields.Char(string='Bidang keahlian S1')
    gelar_s1 = fields.Char(string='Gelar S1')
    asal_pt_s2 = fields.Char(string='Asal PT S2')
    bidang_keahlian_s2 = fields.Char(string='Bidang keahlian S2')
    gelar_s2 = fields.Char(string='Gelar S2')
    asal_pt_s3 = fields.Char(string='Asal PT S3')
    bidang_keahlian_s3 = fields.Char(string='Bidang keahlian S3')
    gelar_s3 = fields.Char(string='Gelar S3')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_432 table
        report.record_3a_432.unlink()

        # Add dosen tetap diluar PS according to prodi
