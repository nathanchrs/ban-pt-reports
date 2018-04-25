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
        sum_ = 0
        count = 0
        thesises = reports.env['itb.academic_thesis'].search([])
        for thesis in thesises:
            start_year, start_month, start_day = thesis.start.split('-')
            finish_year, finish_month, finish_day = thesis.finish.split('-')
            if int(start_year) <= report.year and int(start_year) > report.year -3 and int(finish_year) <= report.year and int(finish_year) > report.year -3:
                sum_ += (int(finish_year) - int(start_year)) * 365
                sum_ += (int(finish_month) - int(start_month)) * 30
                sum_ += (int(finish_day) - int(start_day))
                count += 1
        avg = float(sum_ / count) / 30
        line_1_record_3a_552 = {
            'pertanyaan': 'Rata-rata lama penyelesaian tugas akhir/skripsi pada tiga tahun terakhir :',
            'jawaban': "%.2f" % avg,
            'keterangan': 'bulan',
        }
        report.write({'record_3a_552': [(0, 0, line_1_record_3a_552)]})

        line_2_record_3a_552 = {
            'pertanyaan': 'Menurut kurikulum tugas akhir direncanakan ',
            'jawaban': '2', #default
            'keterangan': 'semester',
        }
        report.write({'record_3a_552': [(0, 0, line_2_record_3a_552)]})
