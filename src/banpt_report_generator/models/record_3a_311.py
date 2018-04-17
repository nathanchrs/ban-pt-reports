# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_311(models.Model):
    _name = 'banpt_report_generator.record_3a_311'
    _rec_name = 'tahun'
    _title = '3A-3.1.1 Data Mahasiswa Reguler'

    tahun = fields.Char(string='Tahun Akademik', required=True)
    daya_tampung = fields.Integer(string='Daya Tampung')
    calon_ikut_seleksi = fields.Integer(string='Calon Mahasiswa Ikut Seleksi')
    calon_lulus_seleksi = fields.Integer(string='Calon Mahasiswa Lulus Seleksi')
    mahasiswa_baru_reguler = fields.Integer(string='Mahasiswa Baru Reguler Bukan Transfer')
    mahasiswa_baru_transfer = fields.Integer(string='Mahasiswa Baru Transfer')
    total_mahasiswa_reguler = fields.Integer(string='Total Mahasiswa Reguler Bukan Transfer')
    total_mahasiswa_transfer = fields.Integer(string='Total Mahasiswa Transfer')
    lulusan_reguler = fields.Integer(string='Lulusan Reguler Bukan Transfer')
    lulusan_transfer = fields.Integer(string='Lulusan Transfer')
    ipk_reguler_min = fields.Float(string='IPK Lulusan Reguler Minimum')
    ipk_reguler_avg = fields.Float(string='IPK Lulusan Reguler Rata-Rata')
    ipk_reguler_max = fields.Float(string='IPK Lulusan Reguler Maksimum')
    persen_ipk_275 = fields.Float(string='Persen Lulusan Reguler, IPK <2.75')
    persen_ipk_275_350 = fields.Float(string='Persen Lulusan Reguler, IPK 2.75-3.50')
    persen_ipk_350 = fields.Float(string='Persen Lulusan Reguler, IPK >3.50')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
