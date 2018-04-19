# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_731(models.Model):
    _name = 'banpt_report_generator.record_3b_731'
    _rec_name = 'program_studi'
    _title = '3B-7.3.1 Not Found'

    program_studi = fields.Text(string='', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
