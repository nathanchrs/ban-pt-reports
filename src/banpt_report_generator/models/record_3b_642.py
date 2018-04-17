# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_642(models.Model):
	_name = 'banpt_report_generator.record_3b_642'
	_rec_name = 'jenis_data'
	_title = '3B-6.4.2 Aksesibilitas Data'

	jenis_data = fields.Char(string='Jenis Data', required=True)
	manual = fields.Boolean(string='Sistem Pengolahan Data Secara Manual')
	komputer_tanpa_jaringan = fields.Boolean(string='Sistem Pengolahan Data Dengan Komputer Tanpa Jaringan')
	komputer_jaringan_lokal = fields.Boolean(string='Sistem Pengolahan Data Dengan Komputer Jaringan Lokal (LAN)')
	komputer_jaringan_luas = fields.Boolean(string='Sistem Pengolahan Data Dengan Komputer Jaringan Luas (WAN)')

	# The report this record belongs to
	report = fields.Many2one(comodel_name='banpt_report_generator.report')
	report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
