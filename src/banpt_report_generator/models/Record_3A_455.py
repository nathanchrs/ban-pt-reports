# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_455(models.Model):
	_name = 'banpt_report_generator.record_3a_455'
	_rec_name = 'nama'
	_title = '3A-4.5.5 Keikutsertaan Dosen Tetap Dalam Organisasi Keilmuan/Profesi'

	nama = fields.Char(string='Nama', required=True)
	nama_organisasi = fields.Text(string='Nama Organisasi Keilmuan atau Organisasi Profesi')
	tahun_awal = fields.Char(string='Kurun Waktu Tahun Awal')
	tahun_akhir = fields.Char(string='Kurun Waktu Tahun Akhir')
	internasional_tingkat = fields.Boolean(string='Tingkat Internasional')
	nasional_tingkat = fields.Boolean(string='Tingkat Nasional')
	lokal_tingkat = fields.Boolean(string='Tingkat Lokal')

	# The report this record belongs to
	report = fields.Many2one(comodel_name='banpt_report_generator.report')
	report_refresh_date = fields.Datetime(related='report.refresh_date')



