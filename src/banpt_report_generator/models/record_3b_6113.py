# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_6113(models.Model):
    _name = 'banpt_report_generator.record_3b_6113'
    _rec_name = 'nama_prodi'
    _title = '3B-6.1.1.3 Penggunaan Dana Untuk Tridarma'

    nama_prodi = fields.Text(string='Jenis Dana', required=True)
    jumlah_dana_ts_2 = fields.Integer(string='Jumlah Dana TS-2 (juta rupiah)')
    jumlah_dana_ts_1 = fields.Integer(string='Jumlah Dana TS-1 (juta rupiah)')
    jumlah_dana_ts = fields.Integer(string='Jumlah Dana TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clean record_3b_6113 table
        report.record_3b_6113.unlink()

        programs = reports.env['itb.academic_program'].search([['id', '=', report.prodi.id]])
        for program in programs:
            new_3b_6113 = {
                'nama_prodi': program.name,
                'jumlah_dana_ts_2': 0, # TODO
                'jumlah_dana_ts_1': 0, # TODO
                'jumlah_dana_ts': 0, # TODO
            }

            report.write({'record_3b_6113': [(0, 0, new_3b_6113)]})
