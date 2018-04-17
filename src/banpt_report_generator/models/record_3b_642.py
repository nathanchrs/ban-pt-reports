# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_642(models.Model):
    _name = 'banpt_report_generator.record_3b_642'
    _rec_name = 'jenis_data'
    _title = '3B-6.4.2 Aksesibilitas Data'

    jenis_data = fields.Char(string='Jenis Data')
    pengolahan_data_manual = fields.Selection([('checklist', 'V')], string='Pengolahan Data Secara Manual')
    pengolahan_data_komputer_tanpa_jaringan = fields.Selection([('checklist', 'V')], string='Dengan Komputer Tanpa Jaringan')
    pengolahan_data_komputer_dengan_lan = fields.Selection([('checklist', 'V')], string='Dengan Komputer jaringan Lokal (LAN)')
    pengolahan_data_komputer_jaringan_luas = fields.Selection([('checklist', 'V')], string='Dengan Komputer jaringan Luas (WAN)')

	# The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
