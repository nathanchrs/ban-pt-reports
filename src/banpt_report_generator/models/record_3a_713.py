# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_713(models.Model):
    _name = 'banpt_report_generator.record_3a_713'
    _rec_name = 'judul'
    _title = '3A-7.1.3 Judul Artikel Ilmiah/Karya Ilmiah/Karya Seni/Buku'

    judul = fields.Text(string='Judul', required=True)
    nama_dosen = fields.Text(string='Nama-nama Dosen')
    tempat_publikasi = fields.Text(string='Dihasilkan/Dipublikasikan Pada')
    tahun_publikasi = fields.Text(string='Tahun Penyajian/Publikasi')
    dosen_lokal = fields.Selection([('checklist', 'V')], string='Banyaknya Dosen Lokal')
    dosen_nasional = fields.Selection([('checklist', 'V')], string='Banyaknya Dosen Nasional')
    dosen_internasional = fields.Selection([('checklist', 'V')], string='Banyaknya Dosen Internasional')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_713 table
        report.record_3a_713.unlink()

        # Add judul artikel ilmiah or others table
