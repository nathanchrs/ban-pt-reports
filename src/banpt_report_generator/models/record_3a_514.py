# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_514(models.Model):
    _name = 'banpt_report_generator.record_3a_514'
    _rec_name = 'not_found'
    _title = '3A-5.1.4 Not Found'

    not_found = fields.Char(string='Not Found', required=True)
    
    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
