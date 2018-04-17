# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

class Record_Dosen(models.Model):
    _name = 'banpt_report_generator.dosen'
    _rec_name = 'nama'
    _title = 'Dosen'

    nama = fields.Char(string='Nama', required=True)
    nidn = fields.Char(string='NIDN')
    tanggal_lahir = fields.Date(string='Tanggal lahir')
    jabatan = fields.Char(string='Jabatan')
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
        # Clear dosen table
        report.dosen.unlink()

        # Add dosen according to prodi
        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]])
        for instructor in instructors:
            education_s1 = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['degree', '=', 'undergraduate']])
            education_s2 = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['degree', '=', 'graduate']])
            education_s3 = reports.env['itb.hr_education'].search([['employee_id', '=', instructor.id], ['degree', '=', 'doctoral']])
            new_dosen = {
                'nama': instructor.name_related,
                'nidn': instructor.nidn or '',
                'tanggal_lahir': instructor.birthday,
                'jabatan': instructor.last_jabatan,
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

            report.write({'dosen': [(0, 0, new_dosen)]})
