# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_652(models.Model):
    _name = 'banpt_report_generator.record_3a_652'
    _rec_name = 'jenis_data'
    _title = '3A-6.5.2 Aksesibilitas Tiap Jenis Data'

    no = fields.Integer(string='No')
    jenis_data = fields.Text(string='Jenis Data')
    pengolahan_data_manual = fields.Text(string='Pengolahan Data Secara Manual')
    pengolahan_data_komputer_tanpa_jaringan = fields.Text(string='Dengan Komputer Tanpa Jaringan')
    pengolahan_data_komputer_dengan_lan = fields.Text(string='Dengan Komputer jaringan Lokal (LAN)')
    pengolahan_data_komputer_jaringan_luas = fields.Text(string='Dengan Komputer jaringan Luas (WAN)')
    
    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
