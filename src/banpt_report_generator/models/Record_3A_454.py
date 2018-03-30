# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_454(models.Model):
	_name = 'banpt_report_generator.record_3a_454'
	_rec_name = 'nama'
	_title = '3A-4.5.4 Pencapai Prestasi/Reputasi Dosen'

	nama = fields.Char(string='Nama', required=True)
	prestasi_yang_dicapai = fields.Text(string='Prestasi yang Dicapai')
	tahun_pencapaian = fields.Char(string='Tahun Pencapaian')
	internasional_tingkat = fields.Boolean(string='Tingkat Internasional')
	nasional_tingkat = fields.Boolean(string='Tingkat Nasional')
	lokal_tingkat = fields.Boolean(string='Tingkat Lokal')

	# The report this record belongs to
	report = fields.Many2one(comodel_name='banpt_report_generator.report')
	report_refresh_date = fields.Datetime(related='report.refresh_date')
