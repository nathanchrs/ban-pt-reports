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
    for report in reports:
        # Clear record_3a_721 table
        report.record_3a_721.unlink()

        #add record_3a_721
        new_record_3a_721 = {
            'sumber_biaya': 'Pembiayaan sendiri oleh dosen',
            'ts_2': 0, #TODO
            'ts_1': 0, #TODO
            'ts': 0, #TODO
        }

        report.write({'record_3a_721': [(0, 0, new_record_3a_721)]})

        #add record_3a_721
        new_record_3a_721 = {
            'sumber_biaya': 'PT yang bersangkutan',
            'ts_2': 3, #TODO
            'ts_1': 3, #TODO
            'ts': 3, #TODO
        }

        report.write({'record_3a_721': [(0, 0, new_record_3a_721)]})

        #add record_3a_721
        new_record_3a_721 = {
            'sumber_biaya': 'Depdiknas',
            'ts_2': 0, #TODO
            'ts_1': 0, #TODO
            'ts': 0, #TODO
        }

        report.write({'record_3a_721': [(0, 0, new_record_3a_721)]})

        #add record_3a_721
        new_record_3a_721 = {
            'sumber_biaya': 'Pembiayaan dalam negeri di luar Depdiknas',
            'ts_2': 1 #TODO
            'ts_1': 2, #TODO
            'ts': 0, #TODO
        }

        report.write({'record_3a_721': [(0, 0, new_record_3a_721)]})

        #add record_3a_721
        new_record_3a_721 = {
            'sumber_biaya': 'Institusi luar negeri',
            'ts_2': 0, #TODO
            'ts_1': 0, #TODO
            'ts': 0, #TODO
        }

        report.write({'record_3a_721': [(0, 0, new_record_3a_721)]})