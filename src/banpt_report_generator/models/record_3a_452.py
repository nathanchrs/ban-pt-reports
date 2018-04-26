# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import utils

class Record_3A_452(models.Model):
    _name = 'banpt_report_generator.record_3a_452'
    _rec_name = 'nama_dosen'
    _title = '3A-4.5.2 Peningkatan Kemampuan Dosen Tetap Melalui Tugas Belajar'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    jenjang_pendidikan = fields.Char(string='Jenjang Pendidikan Lanjut')
    bidang_studi = fields.Char(string='Bidang Studi')
    perguruan_tinggi = fields.Char(string='Perguruan Tinggi')
    negara = fields.Char(string='Negara')
    tahun_pelaksanaan = fields.Char(string='Tahun Pelaksanaan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_452.unlink()

        instructors = reports.env['hr.employee'].search([
            ['is_faculty', '=', True],
            ['prodi', '=', report.prodi.id],
            ['employment_type', '!=', 'contract']
        ]) # TODO: add WHERE statement with dosen_tetap sesuai prodi

        for instructor in instructors:
            instructors_learn = reports.env['itb.hr_education'].search([
                ['employee_id', '=', instructor.id],
            ])

            for instructor_learn in instructors_learn:
                year = False
                if instructor_learn.finish:
                    year = utils.get_year(instructor_learn.finish)
                if int(year) >= report.year - 2:
                    new_record_3a_452 = {
                        'nama_dosen': instructor_learn.employee_id.name_related,
                        'jenjang_pendidikan': instructor_learn.degree,
                        'bidang_studi': instructor_learn.major,
                        'perguruan_tinggi': instructor_learn.school,
                        'negara': instructor_learn.city,
                        'tahun_pelaksanaan': year
                    }

                    report.write({'record_3a_452': [(0, 0, new_record_3a_452)]})
