# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_411(models.Model):
    _name = 'banpt_report_generator.record_3b_411'
    _rec_name = 'hal'
    _title = '3B-4.1.1 Dosen Tetap yang Bidang Keahliannya Sesuai Bidang PS'

    hal = fields.Char(string='Hal', required=True)
    total_di_fakultas = fields.Integer(string='Total di Fakultas')
    ps1_elektro = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-1 Teknik Elektro')
    ps2_informatika = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-2 Teknik Informatika')
    ps3_tenaga_listrik = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-3 Teknik Tenaga Listrik')
    ps4_telekomunikasi = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-4 Teknik Telekomunikasi')
    ps5_sistem_teknologi_informasi = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-5 Sistem & Teknologi Informasi')
    ps6_biomedis = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-6 Teknik Biomedis')

	# The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
