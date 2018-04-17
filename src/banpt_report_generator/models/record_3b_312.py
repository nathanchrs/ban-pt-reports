# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_312(models.Model):
    _name = 'banpt_report_generator.record_3b_312'
    _rec_name = 'jenis_program'
    _title = '3B-3.1.2 Mahasiswa dan Lulusan'

    jenis_program = fields.Char(string='Hal', required=True)
    jenis_mahasiswa = fields.Char(string='Hal')
    total_mahasiswa_fakultas = fields.Integer(string='Total Mahasiswa pada Fakultas')
    jumlah_mahasiswa_ps1 = fields.Integer(string='Nama PS-1')
    jumlah_mahasiswa_ps2 = fields.Integer(string='Nama PS-2')
    jumlah_mahasiswa_ps3 = fields.Integer(string='Nama PS-3')
    jumlah_mahasiswa_ps4 = fields.Integer(string='Nama PS-4')
    jumlah_mahasiswa_ps5 = fields.Integer(string='Sistem & Teknologi Informasi')
    jumlah_mahasiswa_ps6 = fields.Integer(string='Teknik Biomedis')
    jumlah_mahasiswa_ps7 = fields.Integer(string='TPB')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
