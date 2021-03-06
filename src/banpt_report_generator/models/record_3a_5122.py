# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_5122(models.Model):
    _name = 'banpt_report_generator.record_3a_5122'
    _rec_name = 'kode_mk'
    _title = '3A-5.1.2.2 Struktur Kurikulum Berdasarkan Urutan Mata Kuliah'

    smt = fields.Char(string='Semester', required=True)
    kode_mk = fields.Char(string='Kode Mata Kuliah', required=True)
    nama_mk = fields.Text(string='Nama Mata Kuliah', required=True)
    bobot_sks = fields.Integer(string='Bobot SKS', required=True)
    sks_mk_dalam_kurikulum_inti = fields.Char(string='SKS Mata Kuliah Dalam Kurikulum Inti')
    sks_mk_dalam_kurikulum_institusional = fields.Char(string='SKS Mata Kuliah Dalam Kurikulum Institusional')
    bobot_tugas = fields.Char(string='Bobot Tugas')
    kelengkapan_deskripsi = fields.Char(string='Kelengkapan Deskripsi')
    kelengkapan_silabus = fields.Char(string='Kelengkapan Silabus')
    kelengkapan_sap = fields.Char(string='Kelengkapan SAP')
    unit_penyelenggara = fields.Char(string='Unit/Jurusan/Fakultas Penyelenggara', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        #Clear record_3a_5122 table
        report.record_3a_5122.unlink()

        #add record_3a_5122 according to program_id
        program = reports.env['itb.academic_program'].search([['id', '=', report.prodi.id]])
        curriculums = reports.env['itb.academic_curriculum'].search([['program_id', '=', report.prodi.id], ['year', '<=', report.year]], order='year desc', limit=1)
        for curriculum_id in curriculums:
            curriculum_lines = reports.env['itb.academic_curriculum_line'].search([['curriculum_id', '=', curriculum_id.id]], order='semester')
            for curriculum_line in curriculum_lines:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', curriculum_line.catalog_id.id]])
                new_record_3a_5122 = {
                    'smt': curriculum_line.semester if curriculum_line.semester else '0',
                    'kode_mk': catalog[0].code if catalog else '',
                    'nama_mk': catalog[0].name if catalog else '',
                    'bobot_sks': catalog[0].credit if catalog else 0,
                    'sks_mk_dalam_kurikulum_inti': '', # TODO
                    'sks_mk_dalam_kurikulum_institusional': '', # TODO
                    'bobot_tugas': '', # TODO
                    'kelengkapan_deskripsi': 'v' if catalog.note else '',
                    'kelengkapan_silabus': 'v' if catalog.syllabus else '',
                    'kelengkapan_sap': '', # TODO
                    'unit_penyelenggara': program[0].name if program else '',
                }
                report.write({'record_3a_5122': [(0, 0, new_record_3a_5122)]})
