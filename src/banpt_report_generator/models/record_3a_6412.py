# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_6412(models.Model):
    _name = 'banpt_report_generator.record_3a_6412'
    _rec_name = 'nama_jurnal'
    _title = '3A-6.4.1.2 Pustaka'

    jenis_jurnal = fields.Text(string='Jenis')
    no = fields.Integer(string='No')
    nama_jurnal = fields.Text(string='Nama Jurnal')
    rincian_no_tahun = fields.Text(string='Rincian Nomor dan Tahun')
    jumlah_pustaka = fields.Integer(string='Jumlah')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
