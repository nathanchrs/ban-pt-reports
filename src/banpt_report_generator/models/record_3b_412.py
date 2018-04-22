# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_412(models.Model):
    _name = 'banpt_report_generator.record_3b_412'
    _rec_name = 'hal'
    _title = '3B-4.1.2 Penggantian dan Pengembangan Dosen Tetap'

    hal = fields.Char(string='Hal', required=True)
    total_di_fakultas = fields.Integer(string='Total di Fakultas')
    ps1_elektro = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-1 Teknik Elektro')
    ps2_informatika = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-2 Teknik Informatika')
    ps3_tenaga_listrik = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-3 Teknik Tenaga Listrik')
    ps4_telekomunikasi = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-4 Teknik Telekomunikasi')
    ps5_sistem_teknologi_informasi = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-5 Sistem & Teknologi Informasi')
    ps6_biomedis = fields.Integer(string='Jumlah Dosen yang bertugas pada PS-6 Teknik Biomedis')

	# The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3b_412 table
        report.record_3b_412.unlink()

        # Add record_3b_412 data
        ps1, ps2, ps3, ps4, ps5, ps6 = count_employee(reports, 'dosen')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        new_record_3b_412 = {
            'hal': 'Banyaknya dosen pensiun/berhenti',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_412': [(0, 0, new_record_3b_412)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_employee(reports, 'dosen')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        new_record_3b_412 = {
            'hal': 'Banyaknya perekrutan dosen baru',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_412': [(0, 0, new_record_3b_412)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_employee(reports, 'dosen')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        new_record_3b_412 = {
            'hal': 'Banyaknya dosen tugas belajar S2/Sp-1',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_412': [(0, 0, new_record_3b_412)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_employee(reports, 'dosen')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        new_record_3b_412 = {
            'hal': 'Banyaknya dosen tugas belajar S3/Sp-2',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_412': [(0, 0, new_record_3b_412)]})

def count_employee(reports, hal):
    ids_prodi = list()
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Elektro']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Informatika']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Tenaga Listrik']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Telekomunikasi']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Sistem dan Teknologi Informasi']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Biomedika']]).id)

    count_dosen = list()

    for id_prodi in ids_prodi:
        counter = len(reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', id_prodi], ['last_edu', '=', hal]]))
        count_dosen.append(counter)

    return 0, 0, 0, 0, 0, 0
    # return count_dosen[0], count_dosen[1], count_dosen[2], count_dosen[3], count_dosen[4], count_dosen[5]
