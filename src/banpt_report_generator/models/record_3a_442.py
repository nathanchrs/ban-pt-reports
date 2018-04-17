# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_442(models.Model):
    _name = 'banpt_report_generator.record_3a_442'
    _rec_name = 'nama_dosen'
    _title = '3A-4.4.2 Aktivitas Mengajar Data Dosen Tidak Tetap'

    nama_dosen = fields.Char(string='Nama Dosen Tidak Tetap', required=True)
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
        # Clear Record_3A_442 table
        report.record_3a_442.unlink()

        # Add aktivitas mengajar dosen tetap
        semester_even = reports.env['itb.academic_semester'].search([['year', '=', report.year], ['type', '=', 'even']])
        semester_odd = reports.env['itb.academic_semester'].search([['year', '=', report.year - 1], ['type', '=', 'odd']])
        dosen_employees = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]]) # TODO: add WHERE statement with sesuai prodi
        for dosen in dosen_employees:
            instructors_even = reports.env['itb.academic_instructor'].search([['employee_id', '=', dosen.id], ['semester', '=', semester_even.name]])
            instructors_odd = reports.env['itb.academic_instructor'].search([['employee_id', '=', dosen.id], ['semester', '=', semester_odd.name]])
            for instructor_even in instructors_even:
                catalog_even = reports.env['itb.academic_catalog'].search([['id', '=', instructor_even.course_id.catalog_id.id]])
                new_record_3a_442 = {
                    'nama_dosen': dosen.name_related,
                    'kode_matkul': catalog_even.code,
                    'nama_matkul': catalog_even.name,
                    'jumlah_sks_matkul': catalog_even.credit,
                    'jumlah_pertemuan_terencana_matkul': 0, # TODO: find where to get lecture info
                    'jumlah_pertemuan_terlaksana_matkul': 0, # TODO: find where to get lecture info
                }

                report.write({'record_3a_442': [(0, 0, new_record_3a_442)]})
            for instructor_odd in instructors_odd:
                catalog_odd = reports.env['itb.academic_catalog'].search([['id', '=', instructor_odd.course_id.catalog_id.id]])
                new_record_3a_442 = {
                    'nama_dosen': dosen.name_related,
                    'kode_matkul': catalog_odd.code,
                    'nama_matkul': catalog_odd.name,
                    'jumlah_sks_matkul': catalog_odd.credit,
                    'jumlah_pertemuan_terencana_matkul': 0, # TODO: find where to get lecture
                    'jumlah_pertemuan_terlaksana_matkul': 0, # TODO: find where to get lecture
                }

                report.write({'record_3a_442': [(0, 0, new_record_3a_442)]})
