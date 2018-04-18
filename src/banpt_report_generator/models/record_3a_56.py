# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_56(models.Model):
    _name = 'banpt_report_generator.record_3a_56'
    _rec_name = 'nama_dosen'
    _title = '3A-5.6 Not Found'

    nama_dosen = fields.Text(string='', required=True)
    jumlah_mahasiswa_bimbingan = fields.Integer(string='', required=True)
    pertemuan_per_semester = fields.Integer(string='', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass