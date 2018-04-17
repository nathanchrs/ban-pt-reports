# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_453(models.Model):
    _name = 'banpt_report_generator.record_3a_453'
    _rec_name = 'nama_dosen'
    _title = '3A-4.5.3 Kegiatan Dosen Tetap'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    jenis_kegiatan = fields.Char(string='Jenis Kegiatan')
    tempat = fields.Char(string='Tempat')
    tahun = fields.Char(string='Tahun')
    sebagai_penyaji = fields.Selection([('checklist', 'V')], string='Sebagai Penyaji')
    sebagai_peserta = fields.Selection([('checklist', 'V')], string='Sebagai Peserta')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_453
        report.record_3a_453.unlink()

        # Add kegiatan dosen tetap
