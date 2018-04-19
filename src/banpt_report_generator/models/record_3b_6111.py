# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_6111(models.Model):
    _name = 'banpt_report_generator.record_3b_6111'
    _rec_name = 'jenis_dana'
    _title = '3B-6.1.1.1 Jumlah Dana Yang Diterima Fakultas'

    sumber_dana = fields.Text(string='Sumber Dana', required=True)
    jenis_dana = fields.Text(string='Jenis Dana', required=True)
    jumlah_dana_ts_2 = fields.Integer(string='Jumlah Dana TS-2 (juta rupiah)')
    jumlah_dana_ts_1 = fields.Integer(string='Jumlah Dana TS-1 (juta rupiah)')
    jumlah_dana_ts = fields.Integer(string='Jumlah Dana TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
<<<<<<< HEAD
    pass
=======
    for report in reports:
        # Clean record_3b_6111 table
        report.record_3b_6111.unlink()

        # Add record_3b_6111 according to program_id
        programs = reports.env['itb.academic_program'].search([])
        for program in programs:
            new_record_3b_6111 = {
                'sumber_dana': 'dummy',
                'jenis_dana': program.name,
                'jumlah_dana_ts_2': 0, # TODO
                'jumlah_dana_ts_1': 0, # TODO
                'jumlah_dana_ts': 0, # TODO
            }

            report.write({'record_3b_6111': [(0, 0, new_record_3b_6111)]})
>>>>>>> master
