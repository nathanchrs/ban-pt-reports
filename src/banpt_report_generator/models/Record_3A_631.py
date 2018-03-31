# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_631(models.Model):
	_name = 'banpt-report-generator.record_3a_631'
	_rec_name = 'ruang_kerja_dosen'
	_title = '3A-6.3.1 Data Ruang Kerja Dosen Tetap'

	ruang_kerja_dosen = fields.Text(string='Ruang Kerja Dosen')
	jumlah_ruang = fields.Integer(string='Jumlah Ruang')
	jumlah_luas = fields.Integer(string='Jumlah Luas (m2)')

	# The report this record belongs to
	report = fields.Many2one(comodel_name='banpt_report_generator.report')
	report_refresh_date = fields.Datetime(related='report.refresh_date')
