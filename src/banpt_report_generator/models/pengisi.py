# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_Pengisi(models.Model):
    _name = 'banpt_report_generator.pengisi'
    _rec_name = 'nama'
    _title = 'Pengisi'

    nama = fields.Char(string='Nama', required=True)
    nidn = fields.Char(string='NIDN', required=True)
    jabatan = fields.Char(string='Jabatan')
    tanggal_pengisian = fields.Date(default=fields.Date.today())

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
