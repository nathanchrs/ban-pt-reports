# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_411(models.Model):
    _name = 'banpt_report_generator.record_3b_411'
    _rec_name = 'hal'
    _title = '3B-4.1.1 Dosen Tetap yang Bidang Keahliannya Sesuai Bidang PS'

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
        # Clear record_3b_411 table
        report.record_3b_411.unlink()

        # Jabatan fungsional
        total_total = 0
        ps1_total = 0
        ps2_total = 0
        ps3_total = 0
        ps4_total = 0
        ps5_total = 0
        ps6_total = 0

        new_record_3b_411 = {
            'hal': 'Jabatan Fungsional :',
            'total_di_fakultas': None,
            'ps1_elektro': None,
            'ps2_informatika': None,
            'ps3_tenaga_listrik': None,
            'ps4_telekomunikasi': None,
            'ps5_sistem_teknologi_informasi': None,
            'ps6_biomedis': None,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        # Add record_3b_411 data
        ps1, ps2, ps3, ps4, ps5, ps6 = count_jabatan(reports, 'Asisten Ahli')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'Asisten Ahli',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_jabatan(reports, 'Lektor')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'Lektor',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_jabatan(reports, 'Lektor Kepala')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'Lektor Kepala',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_jabatan(reports, 'Guru Besar')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        ps11, ps22, ps33, ps44, ps55, ps66 = count_jabatan(reports, 'Profesor')
        total2 = ps11 + ps22 + ps33 + ps44 + ps55 + ps66

        total += total2
        ps1 += ps11
        ps2 += ps22
        ps3 += ps33
        ps4 += ps44
        ps5 += ps55
        ps6 += ps66

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'Guru Besar/Profesor',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        new_record_3b_411 = {
            'hal': 'TOTAL',
            'total_di_fakultas': total_total,
            'ps1_elektro': ps1_total,
            'ps2_informatika': ps2_total,
            'ps3_tenaga_listrik': ps3_total,
            'ps4_telekomunikasi': ps4_total,
            'ps5_sistem_teknologi_informasi': ps5_total,
            'ps6_biomedis': ps6_total,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        # Pendidikan
        total_total = 0
        ps1_total = 0
        ps2_total = 0
        ps3_total = 0
        ps4_total = 0
        ps5_total = 0
        ps6_total = 0

        new_record_3b_411 = {
            'hal': 'Pendidikan Tertinggi :',
            'total_di_fakultas': None,
            'ps1_elektro': None,
            'ps2_informatika': None,
            'ps3_tenaga_listrik': None,
            'ps4_telekomunikasi': None,
            'ps5_sistem_teknologi_informasi': None,
            'ps6_biomedis': None,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        # Add record_3b_411 data
        ps1, ps2, ps3, ps4, ps5, ps6 = count_pendidikan(reports, 'S1')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'S1',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_pendidikan(reports, 'S2')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'S2/profesi/Sp-1',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        ps1, ps2, ps3, ps4, ps5, ps6 = count_pendidikan(reports, 'S3')
        total = ps1 + ps2 + ps3 + ps4 + ps5 + ps6

        total_total += total
        ps1_total += ps1
        ps2_total += ps2
        ps3_total += ps3
        ps4_total += ps4
        ps5_total += ps5
        ps6_total += ps6

        new_record_3b_411 = {
            'hal': 'S3/Sp-2',
            'total_di_fakultas': total,
            'ps1_elektro': ps1,
            'ps2_informatika': ps2,
            'ps3_tenaga_listrik': ps3,
            'ps4_telekomunikasi': ps4,
            'ps5_sistem_teknologi_informasi': ps5,
            'ps6_biomedis': ps6,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

        new_record_3b_411 = {
            'hal': 'TOTAL',
            'total_di_fakultas': total_total,
            'ps1_elektro': ps1_total,
            'ps2_informatika': ps2_total,
            'ps3_tenaga_listrik': ps3_total,
            'ps4_telekomunikasi': ps4_total,
            'ps5_sistem_teknologi_informasi': ps5_total,
            'ps6_biomedis': ps6_total,
        }
        report.write({'record_3b_411': [(0, 0, new_record_3b_411)]})

def count_jabatan(reports, jabatan):
    ids_prodi = list()
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Elektro']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Informatika']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Tenaga Listrik']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Telekomunikasi']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Sistem dan Teknologi Informasi']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Biomedika']]).id)
    count_dosen = list()

    for id_prodi in ids_prodi:
        counter = len(reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', id_prodi], ['last_jabatan', '=like', jabatan]]))
        count_dosen.append(counter)

    return count_dosen[0], count_dosen[1], count_dosen[2], count_dosen[3], count_dosen[4], count_dosen[5]

def count_pendidikan(reports, pendidikan):
    ids_prodi = list()
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Elektro']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Informatika']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Tenaga Listrik']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Telekomunikasi']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Sistem dan Teknologi Informasi']]).id)
    ids_prodi.append(reports.env['itb.academic_program'].search([['name', '=', 'Teknik Biomedika']]).id)

    count_dosen = list()

    for id_prodi in ids_prodi:
        counter = len(reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', id_prodi], ['last_edu', '=', pendidikan]]))
        count_dosen.append(counter)

    return count_dosen[0], count_dosen[1], count_dosen[2], count_dosen[3], count_dosen[4], count_dosen[5]
