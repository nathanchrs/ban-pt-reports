# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_632(models.Model):
    _name = 'banpt_report_generator.record_3a_632'
    _rec_name = 'jenis_kemampuan'
    _title = '3A-6.3.2 Not Found'

    jenis_kemampuan = fields.Text(string='Jenis Kemampuan')
    tanggapan_sangat_baik = fields.Float(string='Tanggapan Sangat Baik')
    tanggapan_baik = fields.Float(string='Tanggapan Baik')
    tanggapan_cukup = fields.Float(string='Tanggapan Cukup')
    tanggapan_kurang = fields.Float(string='Tanggapan Kurang')
    rencana_tindak_lanjut = fields.Text(string='Rencana Tindak Lanjut oleh Prodi')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
