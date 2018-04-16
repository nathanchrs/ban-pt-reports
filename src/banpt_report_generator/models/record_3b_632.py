# -*- coding: utf-8 -*-

from odoo import models, fields, api

class record_3b_632(models.Model):
	_name = 'banpt_report_generator.record_3b_632'
	_rec_name = ''
	_title = '3B-6.3.2 Prasarana Tambahan dan Investasi'



	# The report this record belongs to
	report = fields.Many2one(comodel_name='banpt_report_generator.report')
	report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass


