# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import utils, constants

class Record_3A_311(models.Model):
    _name = 'banpt_report_generator.record_3a_311'
    _rec_name = 'tahun'
    _title = '3A-3.1.1 Data Mahasiswa Reguler'

    tahun = fields.Char(string='Tahun Akademik', required=True)
    daya_tampung = fields.Integer(string='Daya Tampung')
    calon_ikut_seleksi = fields.Integer(string='Calon Mahasiswa Ikut Seleksi')
    calon_lulus_seleksi = fields.Integer(string='Calon Mahasiswa Lulus Seleksi')
    mahasiswa_baru_reguler = fields.Integer(string='Mahasiswa Baru Reguler Bukan Transfer')
    mahasiswa_baru_transfer = fields.Integer(string='Mahasiswa Baru Transfer')
    total_mahasiswa_reguler = fields.Integer(string='Total Mahasiswa Reguler Bukan Transfer')
    total_mahasiswa_transfer = fields.Integer(string='Total Mahasiswa Transfer')
    lulusan_reguler = fields.Integer(string='Lulusan Reguler Bukan Transfer')
    lulusan_transfer = fields.Integer(string='Lulusan Transfer')
    ipk_reguler_min = fields.Float(string='IPK Lulusan Reguler Minimum')
    ipk_reguler_avg = fields.Float(string='IPK Lulusan Reguler Rata-Rata')
    ipk_reguler_max = fields.Float(string='IPK Lulusan Reguler Maksimum')
    persen_ipk_275 = fields.Float(string='Persen Lulusan Reguler, IPK <2.75')
    persen_ipk_275_350 = fields.Float(string='Persen Lulusan Reguler, IPK 2.75-3.50')
    persen_ipk_350 = fields.Float(string='Persen Lulusan Reguler, IPK >3.50')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear report table for this report
        report.record_3a_311.unlink()

        # Add records according to report table format
        for record_year in range(report.year - 4, report.year + 1):
            two_digit_year = str(record_year)[-2:]

            students = reports.env['res.partner'].search([
                ['is_participant', '=', True],
                ['student_id', '=like', report.prodi.prefix + '_____']
            ])

            total_mahasiswa_reguler = 0
            total_mahasiswa_transfer = 0
            mahasiswa_baru_reguler = 0
            mahasiswa_baru_transfer = 0
            lulusan_reguler = 0
            lulusan_transfer = 0
            ipk_lulusan_reguler_minimum = None
            total_ipk_lulusan_reguler = 0.0
            ipk_lulusan_reguler_maksimum = None
            jumlah_ipk_reguler = 0
            jumlah_ipk_lulusan_reguler_275 = 0
            jumlah_ipk_lulusan_reguler_275_350 = 0
            jumlah_ipk_lulusan_reguler_350 = 0

            for student in students:
                nim_two_digit_year = student.student_id[3:5]

                # Calculate mahasiswa baru info
                if nim_two_digit_year == two_digit_year:
                    if utils.nim_type(student.student_id) == constants.TRANSFER_STUDENT:
                        mahasiswa_baru_transfer = mahasiswa_baru_transfer + 1
                    elif utils.nim_type(student.student_id) == constants.REGULAR_STUDENT:
                        mahasiswa_baru_reguler = mahasiswa_baru_reguler + 1

                # Calculate total mahasiswa info
                if int(nim_two_digit_year) >= int(two_digit_year) and ((not student.graduate_date) or (utils.get_year(student.graduate_date) <= int(record_year))):
                    if utils.nim_type(student.student_id) == constants.TRANSFER_STUDENT:
                        total_mahasiswa_transfer = total_mahasiswa_transfer + 1
                    elif utils.nim_type(student.student_id) == constants.REGULAR_STUDENT:
                        total_mahasiswa_reguler = total_mahasiswa_reguler + 1

                # Calculate lulusan info
                if student.graduate_date and utils.get_year(student.graduate_date) == int(record_year):
                    if utils.nim_type(student.student_id) == constants.TRANSFER_STUDENT:
                        lulusan_transfer = lulusan_transfer + 1
                    elif utils.nim_type(student.student_id) == constants.REGULAR_STUDENT:
                        lulusan_reguler = lulusan_reguler + 1
                        if student.ipk:
                            ipk = float(student.ipk)
                            if ipk_lulusan_reguler_minimum is None or ipk < ipk_lulusan_reguler_minimum:
                                ipk_lulusan_reguler_minimum = ipk
                            if ipk_lulusan_reguler_maksimum is None or ipk > ipk_lulusan_reguler_maksimum:
                                ipk_lulusan_reguler_maksimum = ipk
                            total_ipk_lulusan_reguler = total_ipk_lulusan_reguler + ipk
                            jumlah_ipk_reguler = jumlah_ipk_reguler + 1
                            if ipk < 2.75:
                                jumlah_ipk_lulusan_reguler_275 = jumlah_ipk_lulusan_reguler_275 + 1
                            elif ipk >= 2.75 and ipk <= 3.50:
                                jumlah_ipk_lulusan_reguler_275_350 = jumlah_ipk_lulusan_reguler_275_350 + 1
                            elif ipk > 3.50:
                                jumlah_ipk_lulusan_reguler_350 = jumlah_ipk_lulusan_reguler_350 + 1

            # TODO: daya tampung
            # TODO: calon mahasiswa

            # TODO: all students + lulusan: how to differentiate graduation date for each undergrad/graduate?
            # - If only latest graduation date is saved, data for previous years might be different
            # - Better to split program participation into separate table


            new_record = {
                'tahun': utils.calculate_ts_year(record_year, report.year),
                'mahasiswa_baru_reguler': mahasiswa_baru_reguler,
                'mahasiswa_baru_transfer': mahasiswa_baru_transfer,
                'total_mahasiswa_reguler': total_mahasiswa_reguler,
                'total_mahasiswa_transfer': total_mahasiswa_transfer,
                'lulusan_reguler': lulusan_reguler,
                'lulusan_transfer': lulusan_transfer,
                'ipk_reguler_min': ipk_lulusan_reguler_minimum,
                'ipk_reguler_avg': (total_ipk_lulusan_reguler / jumlah_ipk_reguler) if jumlah_ipk_reguler > 0 else None,
                'ipk_reguler_max': ipk_lulusan_reguler_maksimum,
                'persen_ipk_275': (jumlah_ipk_lulusan_reguler_275 * 100 / jumlah_ipk_reguler) if jumlah_ipk_reguler > 0 else None,
                'persen_ipk_275_350': (jumlah_ipk_lulusan_reguler_275_350 * 100 / jumlah_ipk_reguler) if jumlah_ipk_reguler > 0 else None,
                'persen_ipk_350': (jumlah_ipk_lulusan_reguler_350 * 100 / jumlah_ipk_reguler) if jumlah_ipk_reguler > 0 else None
            }

            report.write({'record_3a_311': [(0, 0, new_record)]})
