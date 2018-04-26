# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_6212(models.Model):
    _name = 'banpt_report_generator.record_3a_6212'
    _rec_name = 'jenis_penggunaan'
    _title = '3A-6.2.1.2 Penggunaan Dana Perolehan dan Alokasi Dana'

    jenis_penggunaan = fields.Text(string='Jenis Penggunaan', required=True)
    penggunaan_ts_2 = fields.Integer(string='Penggunaan TS-2 (juta rupiah)')
    penggunaan_ts_1 = fields.Integer(string='Penggunaan TS-1 (juta rupiah)')
    penggunaan_ts = fields.Integer(string='Penggunaan TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_6212 table
        report.record_3a_6212.unlink()

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Pendidikan',
            'penggunaan_ts_2': 451, #TODO
            'penggunaan_ts_1': 573, #TODO
            'penggunaan_ts': 424, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Penelitian',
            'penggunaan_ts_2': 50, #TODO
            'penggunaan_ts_1': 66, #TODO
            'penggunaan_ts': 90, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Pengabdian kepada Masyarakat',
            'penggunaan_ts_2': 0, #TODO
            'penggunaan_ts_1': 0, #TODO
            'penggunaan_ts': 0, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Investasi Prasarana',
            'penggunaan_ts_2': 186, #TODO
            'penggunaan_ts_1': 80, #TODO
            'penggunaan_ts': 64, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Investasi Sarana',
            'penggunaan_ts_2': 0, #TODO
            'penggunaan_ts_1': 0, #TODO
            'penggunaan_ts': 0, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Investasi SDM',
            'penggunaan_ts_2': 0, #TODO
            'penggunaan_ts_1': 0, #TODO
            'penggunaan_ts': 0, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})

        #add record_3a_6212
        new_record_3a_6212 = {
            'jenis_penggunaan': 'Lain-lain',
            'penggunaan_ts_2': 20, #TODO
            'penggunaan_ts_1': 27, #TODO
            'penggunaan_ts': 75, #TODO
        }

        report.write({'record_3a_6212': [(0, 0, new_record_3a_6212)]})