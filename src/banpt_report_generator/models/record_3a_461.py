# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_461(models.Model):
    _name = 'banpt_report_generator.record_3a_461'
    _rec_name = 'jenis_tenaga_kependidikan'
    _title = '3A-4.6.1 Tenaga Kependidikan'

    jenis_tenaga_kependidikan = fields.Text(string='Jenis Tenaga Kependidikan')
    jumlah_S3 = fields.Integer(string='Pendidikan Terakhir S3')
    jumlah_S2 = fields.Integer(string='Pendidikan Terakhir S2')
    jumlah_S1 = fields.Integer(string='Pendidikan Terakhir S1')
    jumlah_D4 = fields.Integer(string='Pendidikan Terakhir D4')
    jumlah_D3 = fields.Integer(string='Pendidikan Terakhir D3')
    jumlah_D2 = fields.Integer(string='Pendidikan Terakhir D2')
    jumlah_D1 = fields.Integer(string='Pendidikan Terakhir D1')
    jumlah_SMA_SMK = fields.Integer(string='Pendidikan Terakhir SMA/SMK')
    unit_kerja = fields.Text(string='Unit Kerja')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_461.unlink()

        h, w = 5, 8
        count_matrix = [[0 for _ in range(w)] for _ in range(h)]

        instructors = reports.env['hr.employee'].search([])
        for instructor in instructors:
            #Create count matrix (4 Tendik * 8 Pendidikan Terakhir)
            index_i = get_index_from_tendik(instructor.tendik)
            index_j = get_index_from_last_edu(instructor.last_edu)
            count_matrix[index_i][index_j] += 1
            count_matrix[4][index_j] += 1

        line_1_record_3a_461 = {
            'jenis_tenaga_kependidikan': 'Pustakawan',
            'jumlah_S3': count_matrix[0][0],
            'jumlah_S2': count_matrix[0][1],
            'jumlah_S1': count_matrix[0][2],
            'jumlah_D4': count_matrix[0][3],
            'jumlah_D3': count_matrix[0][4],
            'jumlah_D2': count_matrix[0][5],
            'jumlah_D1': count_matrix[0][6],
            'jumlah_SMA_SMK': count_matrix[0][7],
            'unit_kerja': 'UPT Perpustakaan ITB',
        }
        report.write({'record_3a_461': [(0, 0, line_1_record_3a_461)]})

        line_2_record_3a_461 = {
            'jenis_tenaga_kependidikan': 'Laboran/ Teknisi/ Analis/ Operator/ Programmer',
            'jumlah_S3': count_matrix[1][0],
            'jumlah_S2': count_matrix[1][1],
            'jumlah_S1': count_matrix[1][2],
            'jumlah_D4': count_matrix[1][3],
            'jumlah_D3': count_matrix[1][4],
            'jumlah_D2': count_matrix[1][5],
            'jumlah_D1': count_matrix[1][6],
            'jumlah_SMA_SMK': count_matrix[1][7],
            'unit_kerja': 'STEI',
        }
        report.write({'record_3a_461': [(0, 0, line_2_record_3a_461)]})

        line_3_record_3a_461 = {
            'jenis_tenaga_kependidikan': 'Administrasi',
            'jumlah_S3': count_matrix[2][0],
            'jumlah_S2': count_matrix[2][1],
            'jumlah_S1': count_matrix[2][2],
            'jumlah_D4': count_matrix[2][3],
            'jumlah_D3': count_matrix[2][4],
            'jumlah_D2': count_matrix[2][5],
            'jumlah_D1': count_matrix[2][6],
            'jumlah_SMA_SMK': count_matrix[2][7],
            'unit_kerja': 'STEI',
        }
        report.write({'record_3a_461': [(0, 0, line_3_record_3a_461)]})

        line_4_record_3a_461 = {
            'jenis_tenaga_kependidikan': 'Lainnya',
            'jumlah_S3': count_matrix[3][0],
            'jumlah_S2': count_matrix[3][1],
            'jumlah_S1': count_matrix[3][2],
            'jumlah_D4': count_matrix[3][3],
            'jumlah_D3': count_matrix[3][4],
            'jumlah_D2': count_matrix[3][5],
            'jumlah_D1': count_matrix[3][6],
            'jumlah_SMA_SMK': count_matrix[3][7],
            'unit_kerja': 'STEI',
        }
        report.write({'record_3a_461': [(0, 0, line_4_record_3a_461)]})

        line_5_record_3a_461 = {
            'jenis_tenaga_kependidikan': 'Total',
            'jumlah_S3': count_matrix[4][0],
            'jumlah_S2': count_matrix[4][1],
            'jumlah_S1': count_matrix[4][2],
            'jumlah_D4': count_matrix[4][3],
            'jumlah_D3': count_matrix[4][4],
            'jumlah_D2': count_matrix[4][5],
            'jumlah_D1': count_matrix[4][6],
            'jumlah_SMA_SMK': count_matrix[4][7],
            'unit_kerja': '',
        }
        report.write({'record_3a_461': [(0, 0, line_5_record_3a_461)]})

def get_index_from_last_edu(x):
    return {
        'S3': 0,
        'S2': 1,
        'S1': 2,
        'D4': 3,
        'D3': 4,
        'D2': 5,
        'D1': 6,
        'SMA/SMK': 7,
    }.get(x, 7) #7 is default

def get_index_from_tendik(x):
    return {
        'pustakawan': 0,
        'laboran/teknisi/analis/operator/programmer': 1,
        'tenaga administrasi': 2,
        'pramu': 3,
    }.get(x, 3) #3 is default
