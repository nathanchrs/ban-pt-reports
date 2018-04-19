# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import utils, constants

class Record_3A_314(models.Model):
    _name = 'banpt_report_generator.record_3a_314'
    _rec_name = 'tahun_masuk'
    _title = '3A-3.1.4 Jumlah Mahasiswa Reguler 7 Tahun Terakhir'

    tahun_masuk = fields.Char(string='Tahun Masuk', required=True)
    ts6 = fields.Integer(string='TS-6')
    ts5 = fields.Integer(string='TS-5')
    ts4 = fields.Integer(string='TS-4')
    ts3 = fields.Integer(string='TS-3')
    ts2 = fields.Integer(string='TS-2')
    ts1 = fields.Integer(string='TS-1')
    ts = fields.Integer(string='TS')
    lulusan_reguler_sampai_ts = fields.Integer(string='Lulusan Reguler s.d. TS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')


def refresh(reports):
    for report in reports:
        # Clear report table for this report
        report.record_3a_314.unlink()

        # Add records according to report table format
        for record_year in range(report.year - 6, report.year + 1):
            students = reports.env['res.partner'].search([
                ['is_participant', '=', True],
                ['student_id', '=like', report.prodi.prefix + '_____']
            ])

            jumlah_mahasiswa = [0, 0, 0, 0, 0, 0, 0]
            lulusan_sampai_ts = 0

            for student in students:
                if utils.nim_type(student.student_id) == constants.REGULAR_STUDENT:
                    if utils.get_nim_year(student.student_id) == record_year:
                        if utils.nim_type(student.student_id) == constants.REGULAR_STUDENT:
                            for column_year in range(record_year, report.year + 1):
                                if (not student.graduate_date) or (utils.get_year(student.graduate_date) >= int(column_year)):
                                    jumlah_mahasiswa[report.year - column_year] += 1
                        if student.graduate_date and utils.get_year(student.graduate_date) <= report.year:
                            lulusan_sampai_ts += 1

            new_record = {
                'tahun_masuk': utils.calculate_ts_year(record_year, report.year),
                'ts6': jumlah_mahasiswa[6],
                'ts5': jumlah_mahasiswa[5],
                'ts4': jumlah_mahasiswa[4],
                'ts3': jumlah_mahasiswa[3],
                'ts2': jumlah_mahasiswa[2],
                'ts1': jumlah_mahasiswa[1],
                'ts': jumlah_mahasiswa[0],
                'lulusan_reguler_sampai_ts': lulusan_sampai_ts
            }

            report.write({'record_3a_314': [(0, 0, new_record)]})
