# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_461(models.Model):
    _name = 'banpt_report_generator.record_3a_461'
    _rec_name = 'jenis_tenaga_kependidikan'
    _title = '3A-4.6.1 Tenaga Kependidikan'

    jenis_tenaga_kependidikan = fields.Text(string='Jenis Tenaga Kependidikan')
    jumlah_S3 = fields.Integer(string='Pendidikan Terakhir S3')
    Jumlah_S2 = fields.Integer(string='Pendidikan Terakhir S2')
    jumlah_S1 = fields.Integer(string='Pendidikan Terakhir S1')
    jumlah_D4 = fields.Integer(string='Pendidikan Terakhir D4')
    jumlah_D3 = fields.Integer(string='Pendidikan Terakhir D3')
    jumlah_D2 = fields.Integer(string='Pendidikan Terakhir D2')
    jumlah_D1 = fields.Integer(string='Pendidikan Terakhir D1')
    jumlah_SMA_SMK = fields.Integer(string='Pendidikan Terakhir SMA/SMK')
    unit_kerja = fields.Text(string='Unit Kerja')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
