# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_Pengisi(models.Model):
    _name = 'banpt_report_generator.pengisi'
    _rec_name = 'pengisi'
    _title = 'Pengisi'

    pengisi = fields.Many2one(string='Nama', required=True, comodel_name='banpt_report_generator.dosen')
    nidn = fields.Char(string='NIDN', related='pengisi.nidn')
    jabatan = fields.Char(string='Jabatan', related='pengisi.jabatan')
    tanggal_pengisian = fields.Date(default=fields.Date.today())

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

#pylint: disable=unused-argument
def refresh(reports):
    pass
