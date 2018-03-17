# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_Dosen(models.Model):
    _name = 'banpt_report_generator.dosen'
    _rec_name = 'nama'
    _title = 'Dosen'

    nama = fields.Char(string='Nama', required=True)
    nidn = fields.Char(string='NIDN', required=True)
    tanggal_lahir = fields.Date(string='Tanggal lahir')
    jabatan = fields.Char(string='Jabatan')
    gelar_s1 = fields.Char(string='Gelar S1')
    asal_pt_s1 = fields.Char(string='Asal PT S1')
    bidang_keahlian_s1 = fields.Char(string='Bidang keahlian S1')
    gelar_s2 = fields.Char(string='Gelar S2')
    asal_pt_s2 = fields.Char(string='Asal PT S2')
    bidang_keahlian_s2 = fields.Char(string='Bidang keahlian S2')
    gelar_s3 = fields.Char(string='Gelar S3')
    asal_pt_s3 = fields.Char(string='Asal PT S3')
    bidang_keahlian_s3 = fields.Char(string='Bidang keahlian S3')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
