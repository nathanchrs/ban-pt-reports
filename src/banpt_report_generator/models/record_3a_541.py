# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_541(models.Model):
    _name = 'banpt_report_generator.record_3a_541'
    _rec_name = 'nama_dosen'
    _title = '3A-5.4.1 Dosen Pembimbing Akademik dan Jumlah Mahasiswa'

    nama_dosen = fields.Text(string='Nama Dosen Pembimbing Akademik', required=True)
    jumlah_mahasiswa_bimbingan = fields.Integer(string='Jumlah Mahasiswa Bimbingan', required=True)
    pertemuan_per_semester = fields.Integer(string='Rata-rata Banyaknya Pertemuan Mahasiswa/Semester', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_541 table
        report.record_3a_541.unlink()

        # add record_3a_541 according to program_id
        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]])
        for instructor in instructors:
            count = 0
            for thesis in reports.env['itb.academic_thesis'].search([]):
                start_year = thesis.start.split('-')[0]
                finish_year = thesis.finish.split('-')[0]
                if int(start_year) <= report.year and int(start_year) > report.year -3 and int(finish_year) <= report.year and int(finish_year) > report.year -3:
                    if instructor.name_related in thesis.supervisors.split(', '):
                        count += 1
            new_record_3a_541 = {
                'nama_dosen': instructor.name_related,
                'jumlah_mahasiswa_bimbingan': count,
                'pertemuan_per_semester': 0, #TODO
            }

            report.write({'record_3a_541': [(0, 0, new_record_3a_541)]})
