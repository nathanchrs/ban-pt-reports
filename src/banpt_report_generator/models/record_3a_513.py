# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_513(models.Model):
    _name = 'banpt_report_generator.record_3a_513'
    _rec_name = 'kode_mk'
    _title = '3A-5.1.3 Mata Kuliah Pilihan'

    smt = fields.Text(string='Semester', required=True)
    kode_mk = fields.Char(string='Kode Mata Kuliah(pilihan)', required=True)
    nama_mk = fields.Text(string='Nama Mata Kuliah', required=True)
    bobot_sks = fields.Integer(string='Bobot SKS', required=True)
    bobot_tugas = fields.Char(string='Bobot Tugas')
    unit_penyelenggara = fields.Char(string='Unit/Jurusan/Fakultas Penyelenggara', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        #Clear record_3a_513 tabel
        report.record_3a_513.unlink()

        # add record_3a_513 according to program_id
        courses = reports.env['itb.academic_course'].search([['program_id', '=', report.prodi.id]])
        for course in courses:
            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'opsional'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                semester = reports.env['itb.academic_semester'].search([['id', '=', course.semester_id.id]])
                program = reports.env['itb.academic_program'].search([['id', '=', course.program_id.id]])
                new_record_3a_513 = {
                    'smt': semester[0].name if semester else '',
                    'kode_mk': catalog[0].code if catalog else '',
                    'nama_mk': course.name,
                    'bobot_sks': catalog[0].credit if catalog else 0,
                    'bobot_tugas': '', # TODO add bobot tugas in itb.academic_catalog
                    'unit_penyelenggara': program[0].name if program else '',
                }
                report.write({'record_3a_513': [(0, 0, new_record_3a_513)]})

            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'opsional-luar'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                semester = reports.env['itb.academic_semester'].search([['id', '=', course.semester_id.id]])
                program = reports.env['itb.academic_program'].search([['id', '=', course.program_id.id]])
                new_record_3a_513 = {
                    'smt': semester[0].name if semester else '',
                    'kode_mk': catalog[0].code if catalog else '',
                    'nama_mk': course.name,
                    'bobot_sks': catalog[0].credit if catalog else 0,
                    'bobot_tugas': '', # TODO add bobot tugas in itb.academic_catalog
                    'unit_penyelenggara': program[0].name if program else '',
                }
                report.write({'record_3a_513': [(0, 0, new_record_3a_513)]})

            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'opsional-external'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                semester = reports.env['itb.academic_semester'].search([['id', '=', course.semester_id.id]])
                program = reports.env['itb.academic_program'].search([['id', '=', course.program_id.id]])
                new_record_3a_513 = {
                    'smt': semester[0].name if semester else '',
                    'kode_mk': catalog[0].code if catalog else '',
                    'nama_mk': course.name,
                    'bobot_sks': catalog[0].credit if catalog else 0,
                    'bobot_tugas': '', # TODO add bobot tugas in itb.academic_catalog
                    'unit_penyelenggara': program[0].name if program else '',
                }
                report.write({'record_3a_513': [(0, 0, new_record_3a_513)]})
