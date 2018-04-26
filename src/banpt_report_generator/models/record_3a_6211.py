# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_6211(models.Model):
    _name = 'banpt_report_generator.record_3a_6211'
    _rec_name = 'jenis_dana'
    _title = '3A-6.2.1.1 Jenis Dana Perolehan dan Alokasi Dana'

    sumber_dana = fields.Text(string='Sumber Dana', required=True)
    jenis_dana = fields.Text(string='Jenis Dana', required=True)
    jumlah_dana_ts_2 = fields.Integer(string='Jumlah Dana TS-2 (juta rupiah)')
    jumlah_dana_ts_1 = fields.Integer(string='Jumlah Dana TS-1 (juta rupiah)')
    jumlah_dana_ts = fields.Integer(string='Jumlah Dana TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_6211 table
        report.record_3a_6211.unlink()

        #add record_3a_6211
        new_record_3a_6211 = {
            'sumber_dana': 'PT Sendiri',
            'jenis_dana': 'DM', #TODO
            'jumlah_dana_ts_2': 1437, #TODO
            'jumlah_dana_ts_1': 1084, #TODO
            'jumlah_dana_ts': 1021, #TODO
        }

        report.write({'record_3a_6211': [(0, 0, new_record_3a_6211)]})

        new_record_3a_6211 = {
            'sumber_dana': 'Pemerintah Pusat',
            'jenis_dana': 'DIPA', #TODO
            'jumlah_dana_ts_2': 2698, #TODO
            'jumlah_dana_ts_1': 1125, #TODO
            'jumlah_dana_ts': 1056, #TODO
        }

        report.write({'record_3a_6211': [(0, 0, new_record_3a_6211)]})

        new_record_3a_6211 = {
            'sumber_dana': 'Diknas',
            'jenis_dana': 'DIPA IL', #TODO
            'jumlah_dana_ts_2': 1222, #TODO
            'jumlah_dana_ts_1': 742, #TODO
            'jumlah_dana_ts': 350, #TODO
        }

        report.write({'record_3a_6211': [(0, 0, new_record_3a_6211)]})

        new_record_3a_6211 = {
            'sumber_dana': 'Sumber Lain',
            'jenis_dana': 'DIPA', #TODO
            'jumlah_dana_ts_2': 0, #TODO
            'jumlah_dana_ts_1': 0, #TODO
            'jumlah_dana_ts': 0, #TODO
        }

        report.write({'record_3a_6211': [(0, 0, new_record_3a_6211)]})

        new_record_3a_6211 = {
            'sumber_dana': 'Sumber Lain',
            'jenis_dana': 'DM', #TODO
            'jumlah_dana_ts_2': 139, #TODO
            'jumlah_dana_ts_1': 32, #TODO
            'jumlah_dana_ts': 1146, #TODO
        }

        report.write({'record_3a_6211': [(0, 0, new_record_3a_6211)]})