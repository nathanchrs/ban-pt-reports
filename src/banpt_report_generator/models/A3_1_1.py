# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_A3_1_1(models.Model):
    _name = 'banpt_report_generator.A3_1_1'
    _rec_name = 'nama'
    _title = 'A3_1_1'

    tahun = fields.Char(string='Tahun Akademik', required=True)
    daya_tampung = fields.Integer(string='Daya Tampung')
    calon_ikut_seleksi = fields.Integer(string='Ikut Seleksi')
    calon_lulus_seleksi = fields.Integer(string='Lulus Seleksi')
    mahasiswa_baru_reguler = fields.Integer(string='Regular Bukan Transfer')
    mahasiswa_baru_transfer = fields.Integer(string='Transfer')
    total_mahasiswa_reguler = fields.Integer(string='Regular Bukan Transfer')
    total_mahasiswa_transfer = fields.Integer(string='Transfer')
    jumlah_lulusan_reguler = fields.Integer(string='Regular Bukan Transfer')
    jumlah_lulusan_transfer = fields.Integer(string='Transfer')
    ipk_reguler_min = fields.Float(string='Min')
    ipk_reguler_avg = fields.Float(string='Rat')
    ipk_reguler_max = fields.Float(string='Mak')
    persen_ipk_275 = fields.Float(string='<2.75')
    persen_ipk_275_350 = fields.Float(string='2.75-3.50')
    persen_ipk_350 = fields.Float(string='>3.50')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
