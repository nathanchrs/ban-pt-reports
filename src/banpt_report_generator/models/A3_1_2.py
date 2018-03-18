# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_A3_1_2(models.Model):
    _name = 'banpt_report_generator.A3_1_2'
    _rec_name = 'nama'
    _title = 'A3_1_2'

    tahun = fields.Char(string='Tahun Akademik', required=True)
    daya_tampung = fields.Integer(string='Daya Tampung')
    calon_ikut_seleksi = fields.Integer(string='Ikut Seleksi')
    calon_lulus_seleksi = fields.Integer(string='Lulus Seleksi')
    mahasiswa_baru_nonreguler = fields.Integer(string='Non Reguler')
    mahasiswa_baru_transfer = fields.Integer(string='Transfer')
    total_mahasiswa_nonreguler = fields.Integer(string='Non Reguler')
    total_mahasiswa_transfer = fields.Integer(string='Transfer')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
