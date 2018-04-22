# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import constants

class Record_3A_434(models.Model):
    _name = 'banpt_report_generator.record_3a_434'
    _rec_name = 'nama_dosen'
    _title = '3A-4.3.4 Aktivitas Mengajar Dosen Tetap yang Bidang Keahliannya Sesuai Dengan PS'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    kode_matkul = fields.Char(string='Kode Mata Kuliah')
    nama_matkul = fields.Char(string='Nama Mata Kuliah')
    jumlah_sks_matkul = fields.Integer(string='Jumlah SKS')
    jumlah_pertemuan_terencana_matkul = fields.Integer(string='Jumlah Pertemuan Direncanakan')
    jumlah_pertemuan_terlaksana_matkul = fields.Integer(string='Jumlah Pertemuan Dilaksanakan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_434
        report.record_3a_434.unlink()

        # Add aktivitas mengajar dosen tetap
        semester_even = reports.env['itb.academic_semester'].search([
            ['year', '=', report.year],
            ['type', '=', 'even']
        ])

        semester_odd = reports.env['itb.academic_semester'].search([
            ['year', '=', report.year - 1],
            ['type', '=', 'odd']
        ])

        dosen_employees = reports.env['hr.employee'].search([
            ['is_faculty', '=', True],
            ['prodi', '=', report.prodi.id]
        ]) # TODO: add WHERE statement with sesuai prodi

        for dosen in dosen_employees:
            instructors_even = reports.env['itb.academic_instructor'].search([
                ['employee_id', '=', dosen.id],
                ['semester', '=', semester_even.name]
            ])

            instructors_odd = reports.env['itb.academic_instructor'].search([
                ['employee_id', '=', dosen.id],
                ['semester', '=', semester_odd.name]
            ])

            for instructor_even in instructors_even:
                catalog_even = reports.env['itb.academic_catalog'].search([
                    ['id', '=', instructor_even.course_id.catalog_id.id]
                ])

                pertemuan_terlaksana_even = 0

                lectures_even = reports.env['itb.academic_lecture'].search([
                    ['course_id', '=', instructor_even.course_id.id]
                ])
                pertemuan_terlaksana_even = len(lectures_even)

                new_record_3a_434 = {
                    'nama_dosen': dosen.name_related,
                    'kode_matkul': catalog_even.code,
                    'nama_matkul': catalog_even.name,
                    'jumlah_sks_matkul': catalog_even.credit,
                    'jumlah_pertemuan_terencana_matkul': ((catalog_even.credit + 1) // 2) * constants.LECTURE_PER_CREDIT,
                    'jumlah_pertemuan_terlaksana_matkul': pertemuan_terlaksana_even,
                }

                report.write({'record_3a_434': [(0, 0, new_record_3a_434)]})
            for instructor_odd in instructors_odd:
                catalog_odd = reports.env['itb.academic_catalog'].search([
                    ['id', '=', instructor_odd.course_id.catalog_id.id]
                ])

                pertemuan_terlaksana_odd = 0

                lectures_odd = reports.env['itb.academic_lecture'].search([
                    ['course_id', '=', instructor_odd.course_id.id]
                ])
                pertemuan_terlaksana_odd = len(lectures_odd)

                new_record_3a_434 = {
                    'nama_dosen': dosen.name_related,
                    'kode_matkul': catalog_odd.code,
                    'nama_matkul': catalog_odd.name,
                    'jumlah_sks_matkul': catalog_odd.credit,
                    'jumlah_pertemuan_terencana_matkul': ((catalog_odd.credit + 1) // 2) * constants.LECTURE_PER_CREDIT,
                    'jumlah_pertemuan_terlaksana_matkul': pertemuan_terlaksana_odd,
                }

                report.write({'record_3a_434': [(0, 0, new_record_3a_434)]})
