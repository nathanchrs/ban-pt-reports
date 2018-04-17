# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_711(models.Model):
    _name = 'banpt_report_generator.record_3a_711'
    _rec_name = 'sumber_biaya'
    _title = '3A-7.1.1 Penelitian Dosen Tetap'

    sumber_biaya = fields.Text(string='Sumber Pembiayaan')
    ts_2 = fields.Integer(string='TS-2')
    ts_1 = fields.Integer(string='TS-1')
    ts = fields.Integer(string='TS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
