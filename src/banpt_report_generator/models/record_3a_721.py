# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_721(models.Model):
    _name = 'banpt_report_generator.record_3a_721'
    _rec_name = 'sumber_dana'
    _title = '3A-7.2.1 Kegiatan Pelayanan/Pengabdian Pada Masyarakat (PKM)'

    sumber_dana = fields.Text(string='Sumber Dana Kegiatan Pelayanan/Pengabdian pada Masyarakat')
    ts_2 = fields.Integer(string='TS-2')
    ts_1 = fields.Integer(string='TS-1')
    ts = fields.Integer(string='TS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_721.unlink()

        line_1_record_3a_721 = {
            'sumber_dana': 'Pembiayaan sendiri oleh peneliti',
            'ts_2': 0, # TODO: just dummy data
            'ts_1': 0, # TODO: just dummy data
            'ts': 0, # TODO: just dummy data
        }
        report.write({'record_3a_721': [(0, 0, line_1_record_3a_721)]})

        line_2_record_3a_721 = {
            'sumber_dana': 'PT yang bersangkutan',
            'ts_2': 0, # TODO: just dummy data
            'ts_1': 0, # TODO: just dummy data
            'ts': 0, # TODO: just dummy data
        }
        report.write({'record_3a_721': [(0, 0, line_2_record_3a_721)]})

        line_3_record_3a_721 = {
            'sumber_dana': 'Depdiknas',
            'ts_2': 0, # TODO: just dummy data
            'ts_1': 0, # TODO: just dummy data
            'ts': 0, # TODO: just dummy data
        }
        report.write({'record_3a_721': [(0, 0, line_3_record_3a_721)]})

        line_4_record_3a_721 = {
            'sumber_dana': 'Institusi dalam negeri di luar Depdiknas',
            'ts_2': 0, # TODO: just dummy data
            'ts_1': 0, # TODO: just dummy data
            'ts': 0, # TODO: just dummy data
        }
        report.write({'record_3a_721': [(0, 0, line_4_record_3a_721)]})

        line_5_record_3a_721 = {
            'sumber_dana': 'Institusi luar negeri',
            'ts_2': 0, # TODO: just dummy data
            'ts_1': 0, # TODO: just dummy data
            'ts': 0, # TODO: just dummy data
        }
        report.write({'record_3a_721': [(0, 0, line_5_record_3a_721)]})
