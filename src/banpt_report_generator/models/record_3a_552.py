# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_552(models.Model):
    _name = 'banpt_report_generator.record_3a_552'
    _rec_name = 'pertanyaan'
    _title = '3A-5.5.2 Penyelesaian Tugas Akhir atau Skripsi'

    pertanyaan = fields.Text(string='', required=True)
    jawaban = fields.Text(string='', required=True)
    keterangan = fields.Text(string='', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_552.unlink()

        line_1_record_3a_552 = {
            'pertanyaan': 'Rata-rata lama penyelesaian tugas akhir/skripsi pada tiga tahun terakhir :',
            'jawaban': '',
            'keterangan': 'bulan',
        }
        report.write({'record_3a_552': [(0, 0, line_1_record_3a_552)]})

        line_2_record_3a_552 = {
            'pertanyaan': 'Menurut kurikulum tugas akhir direncanakan ',
            'jawaban': '',
            'keterangan': 'semester',
        }
        report.write({'record_3a_552': [(0, 0, line_2_record_3a_552)]})
