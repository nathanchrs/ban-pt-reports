# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_435(models.Model):
    _name = 'banpt_report_generator.record_3a_435'
    _rec_name = 'nama_dosen'
    _title = '3A-4.3.5 Aktivitas Mengajar Dosen Tetap yang Bidang Keahliannya Di Luar PS'

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
        # Clear Record_3A_435 tables
        report.record_3a_435.unlink()

        # Add aktivitas mengajar dosen tetap
        semester_even = reports.env['itb.academic_semester'].search([['year', '=', report.year], ['type', '=', 'even']])
        semester_odd = reports.env['itb.academic_semester'].search([['year', '=', report.year - 1], ['type', '=', 'odd']])
        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]]) # TODO: add WHERE statement with tidak sesuai prodi
        for instructor in instructors:
            course_evens = reports.env['itb.academic_course'].search([['semester_id', '=', semester_even.id], ['program_id', '=', 11]]) # TODO: change to instructor_id
            course_odds = reports.env['itb.academic_course'].search([['semester_id', '=', semester_odd.id], ['program_id', '=', 11]]) # TODO: change to instructor_id
            for course_even in course_evens:
                catalog_even = reports.env['itb.academic_catalog'].search([['id', '=', course_even.catalog_id.id]])
                new_record_3a_435 = {
                    'nama_dosen': instructor.name_related,
                    'kode_matkul': catalog_even.code,
                    'nama_matkul': catalog_even.name,
                    'jumlah_sks_matkul': catalog_even.credit,
                    'jumlah_pertemuan_terencana_matkul': 0, # TODO: find where to get lecture info
                    'jumlah_pertemuan_terlaksana_matkul': 0, # TODO: find where to get lecture info
                }

                report.write({'record_3a_435': [(0, 0, new_record_3a_435)]})
            for course_odd in course_odds:
                catalog_odd = reports.env['itb.academic_catalog'].search([['id', '=', course_odd.catalog_id.id]])
                new_record_3a_435 = {
                    'nama_dosen': instructor.name_related,
                    'kode_matkul': catalog_odd.code,
                    'nama_matkul': catalog_odd.name,
                    'jumlah_sks_matkul': catalog_odd.credit,
                    'jumlah_pertemuan_terencana_matkul': 0, # TODO: find where to get lecture
                    'jumlah_pertemuan_terlaksana_matkul': 0, # TODO: find where to get lecture
                }

                report.write({'record_3a_435': [(0, 0, new_record_3a_435)]})
