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
    for report in reports:
        # Clear record_3a_711 table
        report.record_3a_711.unlink()

        #add record_3a_711
        new_record_3a_711 = {
            'sumber_biaya': 'Pembiayaan sendiri oleh peneliti',
            'ts_2': 0, #TODO
            'ts_1': 0, #TODO
            'ts': 0, #TODO
        }

        report.write({'record_3a_711': [(0, 0, new_record_3a_711)]})

        #add record_3a_711
        new_record_3a_711 = {
            'sumber_biaya': 'PT yang bersangkutan',
            'ts_2': 5, #TODO
            'ts_1': 5, #TODO
            'ts': 3, #TODO
        }

        report.write({'record_3a_711': [(0, 0, new_record_3a_711)]})

        #add record_3a_711
        new_record_3a_711 = {
            'sumber_biaya': 'Depdiknas',
            'ts_2': 12, #TODO
            'ts_1': 8, #TODO
            'ts': 17, #TODO
        }

        report.write({'record_3a_711': [(0, 0, new_record_3a_711)]})

        #add record_3a_711
        new_record_3a_711 = {
            'sumber_biaya': 'Institusi dalam negeri di luar Depdiknas',
            'ts_2': 0, #TODO
            'ts_1': 1, #TODO
            'ts': 1, #TODO
        }

        report.write({'record_3a_711': [(0, 0, new_record_3a_711)]})

        #add record_3a_711
        new_record_3a_711 = {
            'sumber_biaya': 'Institusi luar negeri',
            'ts_2': 0, #TODO
            'ts_1': 0, #TODO
            'ts': 0, #TODO
        }

        report.write({'record_3a_711': [(0, 0, new_record_3a_711)]})