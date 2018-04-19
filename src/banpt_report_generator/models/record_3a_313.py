# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_313(models.Model):
    _name = 'banpt_report_generator.record_3a_313'
    _rec_name = 'tahun'
    _title = '3A-3.1.3 Not Found'

    tahun = fields.Char(string='Tahun Akademik', required=True)
    daya_tampung = fields.Integer(string='Daya Tampung')
    calon_ikut_seleksi = fields.Integer(string='Calon Mahasiswa Ikut Seleksi')
    calon_lulus_seleksi = fields.Integer(string='Calon Mahasiswa Lulus Seleksi')
    mahasiswa_baru_nonreguler = fields.Integer(string='Mahasiswa Baru Non-Reguler')
    mahasiswa_baru_transfer = fields.Integer(string='Mahasiswa Baru Transfer')
    total_mahasiswa_nonreguler = fields.Integer(string='Total Mahasiswa Non-Reguler')
    total_mahasiswa_transfer = fields.Integer(string='Total Mahasiswa Transfer')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
