# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import utils, constants

class Record_3A_312(models.Model):
    _name = 'banpt_report_generator.record_3a_312'
    _rec_name = 'tahun'
    _title = '3A-3.1.2 Data Mahasiswa Non-Reguler'

    tahun = fields.Char(string='Tahun Akademik', required=True)
    daya_tampung = fields.Integer(string='Daya Tampung')
    calon_ikut_seleksi = fields.Integer(string='Calon Mahasiswa Ikut Seleksi')
    calon_lulus_seleksi = fields.Integer(string='Calon Mahasiswa Lulus Seleksi')
    mahasiswa_baru_nonreguler = fields.Integer(string='Mahasiswa Baru Non-Reguler')
    mahasiswa_baru_transfer = fields.Integer(string='Mahasiswa Baru Transfer')
    total_mahasiswa_nonreguler = fields.Integer(string='Total Mahasiswa Non-Reguler')
    total_mahasiswa_transfer = fields.Integer(string='Total Mahasiswa Transfer')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')


def refresh(reports):
    for report in reports:
        # Clear report table for this report
        report.record_3a_312.unlink()

        # Add records according to report table format
        for record_year in range(report.year - 4, report.year + 1):
            students = reports.env['res.partner'].search([
                ['is_participant', '=', True],
                ['student_id', '=like', report.prodi.prefix + '_____']
            ])

            total_mahasiswa_nonreguler = 0
            total_mahasiswa_transfer = 0
            mahasiswa_baru_nonreguler = 0
            mahasiswa_baru_transfer = 0

            for student in students:                
                # Calculate mahasiswa baru info
                if utils.get_nim_year(student.student_id) == record_year:
                    if utils.nim_type(student.student_id) == constants.TRANSFER_STUDENT:
                        mahasiswa_baru_transfer += 1
                    elif utils.nim_type(student.student_id) == constants.NONREGULAR_STUDENT:
                        mahasiswa_baru_nonreguler = mahasiswa_baru_nonreguler + 1

                # Calculate total mahasiswa info
                if utils.get_nim_year(student.student_id) >= record_year and ((not student.graduate_date) or (utils.get_year(student.graduate_date) > int(record_year))):
                    if utils.nim_type(student.student_id) == constants.TRANSFER_STUDENT:
                        total_mahasiswa_transfer += 1
                    elif utils.nim_type(student.student_id) == constants.NONREGULAR_STUDENT:
                        total_mahasiswa_nonreguler += 1

            # TODO: daya tampung
            # TODO: calon mahasiswa

            new_record = {
                'tahun': utils.calculate_ts_year(record_year, report.year),
                'mahasiswa_baru_nonreguler': mahasiswa_baru_nonreguler,
                'mahasiswa_baru_transfer': mahasiswa_baru_transfer,
                'total_mahasiswa_nonreguler': total_mahasiswa_nonreguler,
                'total_mahasiswa_transfer': total_mahasiswa_transfer
            }

            report.write({'record_3a_312': [(0, 0, new_record)]})
