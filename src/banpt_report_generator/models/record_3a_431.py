# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_431(models.Model):
    _name = 'banpt_report_generator.record_3a_431'
    _rec_name = 'nama'
    _title = '3A-4.3.1 Dosen Tetap yang Bidang Keahliannya Sesuai Bidang PS'

    nama = fields.Char(string='Nama Dosen Tetap', required=True)
    nidn = fields.Char(string='NIDN', required=True)
    tanggal_lahir = fields.Date(string='Tanggal lahir')
    jabatan = fields.Char(string='Jabatan')
    sertifikasi = fields.Selection([('ya', 'Ya'), ('tidak', 'Tidak')], string='Sertifikasi (Ya/Tidak)')
    gelar_s1 = fields.Char(string='Gelar S1')
    asal_pt_s1 = fields.Char(string='Asal PT S1')
    bidang_keahlian_s1 = fields.Char(string='Bidang keahlian S1')
    gelar_s2 = fields.Char(string='Gelar S2')
    asal_pt_s2 = fields.Char(string='Asal PT S2')
    bidang_keahlian_s2 = fields.Char(string='Bidang keahlian S2')
    gelar_s3 = fields.Char(string='Gelar S3')
    asal_pt_s3 = fields.Char(string='Asal PT S3')
    bidang_keahlian_s3 = fields.Char(string='Bidang keahlian S3')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_431 table
        report.record_3a_431.unlink()

        # Add dosen tetap sesuai PS according to prodi
        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]]) # TODO; add WHERE statement with sesuai prodi
        for instructor in instructors:
            education_s1 = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['degree', '=', 'undergraduate']])
            education_s2 = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['degree', '=', 'graduate']])
            education_s3 = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['degree', '=', 'doctoral']])
            certificate = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['certificate_signer', '!=', '']])
            new_record_3a_431 = {
                'nama': instructor.name_related,
                'nidn': instructor.nidn or '',
                'tanggal_lahir': instructor.birthday,
                'jabatan': instructor.last_jabatan,
                'sertifikasi' : 'ya' if certificate else 'tidak', # TODO: still assumption
                'gelar_s1': '', # TODO: add gelar field in itb.hr_education
                'asal_pt_s1': education_s1[0].school if education_s1 else '',
                'bidang_keahlian_s1': education_s1[0].major if education_s1 else '',
                'gelar_s2': '',  # TODO: add gelar field in itb.hr_education
                'asal_pt_s2': education_s2[0].school if education_s2 else '',
                'bidang_keahlian_s2': education_s2[0].major if education_s2 else '',
                'gelar_s3': '',  # TODO: add gelar field in itb.hr_education
                'asal_pt_s3': education_s3[0].school if education_s3 else '',
                'bidang_keahlian_s3': education_s3[0].major if education_s3 else '',
            }

            report.write({'record_3a_431': [(0, 0, new_record_3a_431)]})
