# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_732(models.Model):
    _name = 'banpt_report_generator.record_3a_732'
    _rec_name = 'not_found'
    _title = '3A-7.3.2 Not Found'

    not_found = fields.Char(string='Nama Dosen Tetap', required=True)
    sks_ps_sendiri = fields.Integer(string='SKS Pengajaran Pada PS Sendiri')
    sks_ps_lain_pt_sendiri = fields.Integer(string='SKS Pengajaran Pada PS Lain, PT Sendiri')
    sks_pt_lain = fields.Integer(string='SKS Pengajaran Pada PT Lain')
    sks_penelitian = fields.Integer(string='SKS Penelitian')
    sks_pengmas = fields.Integer(string='SKS Pengabdian Pada Masyarakat')
    sks_mgmt_pt_sendiri = fields.Integer(string='SKS Manajemen PT Sendiri')
    sks_mgmt_pt_lain = fields.Integer(string='SKS Manajemen PT Lain')
    sks_total = fields.Integer(string='Jumlah SKS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
