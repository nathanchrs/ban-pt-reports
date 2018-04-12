# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_712(models.Model):
    _name = 'banpt_report_generator.record_3a_712'
    _rec_name = 'mhs_ta_penelitian_dosen'
    _title = '3A-7.1.2 Penelitian Dosen Tetap'

    mhs_ta_penelitian_dosen = fields.Selection([('ada', 'Ada'), ('tidak', 'Tidak')], string='Adakah mahasiswa TA yang dilibatkan pada penelitian dosen di 3 tahun terakhir?', required=True)
    jml_mhs_ta_penelitian_dosen = fields.Integer(string='Mahasiswa TA yang dilibatkan penelitian dosen (Jika Ada)')
    jml_mhs_ta_total = fields.Integer(string='Mahasiswa TA total')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
