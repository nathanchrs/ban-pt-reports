# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_631(models.Model):
    _name = 'banpt_report_generator.record_3a_631'
    _rec_name = 'ruang_kerja_dosen'
    _title = '3A-6.3.1 Data Ruang Kerja Dosen Tetap'

    ruang_kerja_dosen = fields.Text(string='Ruang Kerja Dosen')
    jumlah_ruang = fields.Integer(string='Jumlah Ruang')
    jumlah_luas = fields.Integer(string='Jumlah Luas (m2)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_631 table
        report.record_3a_631.unlink()

        #add record_3a_631
        new_record_3a_631 = {
            'ruang_kerja_dosen': 'Satu ruang untuk lebih dari 4 dosen',
            'jumlah_ruang': 0, #TODO
            'jumlah_luas': 0, #TODO
        }

        report.write({'record_3a_631': [(0, 0, new_record_3a_631)]})

        #add record_3a_631
        new_record_3a_631 = {
            'ruang_kerja_dosen': 'Satu ruang untuk 3-4 dosen',
            'jumlah_ruang': 3, #TODO
            'jumlah_luas': 174, #TODO
        }

        report.write({'record_3a_631': [(0, 0, new_record_3a_631)]})

        #add record_3a_631
        new_record_3a_631 = {
            'ruang_kerja_dosen': 'Satu ruang untuk 2 dosen',
            'jumlah_ruang': 1, #TODO
            'jumlah_luas': 60, #TODO
        }

        report.write({'record_3a_631': [(0, 0, new_record_3a_631)]})

        #add record_3a_631
        new_record_3a_631 = {
            'ruang_kerja_dosen': 'Satu ruang untuk 1 dosen (bukan pejabat struktural)',
            'jumlah_ruang': 2, #TODO
            'jumlah_luas': 48, #TODO
        }

        report.write({'record_3a_631': [(0, 0, new_record_3a_631)]})