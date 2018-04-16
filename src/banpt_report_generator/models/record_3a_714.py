# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_714(models.Model):
    _name = 'banpt_report_generator.record_3a_714'
    _rec_name = 'karya_haki'
    _title = '3A-7.1.4 Hak Atas Kekayaan Intelektual'

    karya_haki = fields.Text(string='Karya', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
