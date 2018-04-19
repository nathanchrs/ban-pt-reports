# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_6411(models.Model):
    _name = 'banpt_report_generator.record_3a_6411'
    _rec_name = 'jenis_pustaka'
    _title = '3A-6.4.1.1 Pustaka'

    jenis_pustaka = fields.Text(string='Jenis Pustaka')
    jumlah_judul = fields.Integer(string='Jumlah Judul')
    jumlah_copy = fields.Integer(string='Jumlah Copy')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_6411 table
        report.record_3a_6411.unlink()

        #add record_3a_6411
        new_record_3a_6411 = {
            'jenis_pustaka': 'Buku Teks',
            'jumlah_judul': 3762,
            'jumlah_copy': 9140,
        }

        report.write({'record_3a_6411': [(0, 0, new_record_3a_6411)]})

        new_record_3a_6411 = {
            'jenis_pustaka': 'Jurnal Nasional Yang Terakreditasi',
            'jumlah_judul': 6,
            'jumlah_copy': 0,
        }

        report.write({'record_3a_6411': [(0, 0, new_record_3a_6411)]})

        new_record_3a_6411 = {
            'jenis_pustaka': 'Jurnal Internasional',
            'jumlah_judul': 18,
            'jumlah_copy': 0,
        }

        report.write({'record_3a_6411': [(0, 0, new_record_3a_6411)]})

        new_record_3a_6411 = {
            'jenis_pustaka': 'Prosiding',
            'jumlah_judul': 48,
            'jumlah_copy': 0,
        }

        report.write({'record_3a_6411': [(0, 0, new_record_3a_6411)]})

        new_record_3a_6411 = {
            'jenis_pustaka': 'Skripsi/Tesis',
            'jumlah_judul': 6,
            'jumlah_copy': 0,
        }

        report.write({'record_3a_6411': [(0, 0, new_record_3a_6411)]})

        new_record_3a_6411 = {
            'jenis_pustaka': 'Disertasi',
            'jumlah_judul': 21,
            'jumlah_copy': 30,
        }

        report.write({'record_3a_6411': [(0, 0, new_record_3a_6411)]})
