# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_5121(models.Model):
    _name = 'banpt_report_generator.record_3a_5121'
    _rec_name = 'jenis_mata_kuliah'
    _title = '3A-5.1.2.1 Jumlah SKS Mata Kuliah Wajib dan Pilihan'

    jenis_mata_kuliah = fields.Text(string='Jenis Mata Kuliah', required=True)
    sks = fields.Integer(string='SKS')
    keterangan = fields.Text(string='Keterangan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_5121 table
        report.record_3a_5121.unlink()

        wajib = 0

        courses = reports.env['itb.academic_course'].search([['program_id', '=', report.prodi.id]])
        for course in courses:
            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'wajib'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                wajib += catalog[0].credit

        pilihan = 0

        courses = reports.env['itb.academic_course'].search([['program_id', '=', report.prodi.id]])
        for course in courses:
            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'opsional'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                pilihan += catalog[0].credit

        courses = reports.env['itb.academic_course'].search([['program_id', '=', report.prodi.id]])
        for course in courses:
            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'opsional-external'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                pilihan += catalog[0].credit

        courses = reports.env['itb.academic_course'].search([['program_id', '=', report.prodi.id]])
        for course in courses:
            optional_courses = reports.env['itb.academic_curriculum_line'].search([['catalog_id', '=', course.catalog_id.id], ['category', '=', 'opsional-luar'], ['year', '=', report.year]])
            for optional in optional_courses:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', optional.catalog_id.id]])
                pilihan += catalog[0].credit

        # Add record_3a_5121 according to program_id
        new_record_3a_5121 = {
            'jenis_mata_kuliah': 'Wajib',
            'sks': wajib,
            'keterangan': '',
        }
        report.write({'record_3a_5121': [(0, 0, new_record_3a_5121)]})

        new_record_3a_5121 = {
            'jenis_mata_kuliah': 'Pilihan',
            'sks': pilihan,
            'keterangan': '',
        }
        report.write({'record_3a_5121': [(0, 0, new_record_3a_5121)]})
