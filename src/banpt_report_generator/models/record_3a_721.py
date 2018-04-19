# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_721(models.Model):
    _name = 'banpt_report_generator.record_3a_721'
    _rec_name = 'sumber_dana'
    _title = '3A-7.2.1 Kegiatan Pelayanan/Pengabdian Pada Masyarakat (PKM)'

    sumber_dana = fields.Text(string='Sumber Dana Kegiatan Pelayanan/Pengabdian pada Masyarakat', required=True)
    ts_2 = fields.Integer(string='TS-2')
    ts_1 = fields.Integer(string='TS-1')
    ts = fields.Integer(string='TS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
