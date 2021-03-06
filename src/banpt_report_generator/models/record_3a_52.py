# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_52(models.Model):
    _name = 'banpt_report_generator.record_3a_52'
    _rec_name = 'not_found'
    _title = '3A-5.2 Not Found'

    not_found = fields.Char(string='Not Found', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
