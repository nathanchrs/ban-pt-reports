# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_642(models.Model):
    _name = 'banpt_report_generator.record_3b_642'
    _rec_name = 'jenis_data'
    _title = '3B-6.4.2 Aksesibilitas Data'

    jenis_data = fields.Char(string='Jenis Data')
    pengolahan_data_manual = fields.Selection([('checklist', 'V')], string='Pengolahan Data Secara Manual')
    pengolahan_data_komputer_tanpa_jaringan = fields.Selection([('checklist', 'V')], string='Dengan Komputer Tanpa Jaringan')
    pengolahan_data_komputer_dengan_lan = fields.Selection([('checklist', 'V')], string='Dengan Komputer jaringan Lokal (LAN)')
    pengolahan_data_komputer_jaringan_luas = fields.Selection([('checklist', 'V')], string='Dengan Komputer jaringan Luas (WAN)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3b_642.unlink()

        line_1_record_3b_642 = {
            'jenis_data': 'Mahasiswa',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_1_record_3b_642)]})

        line_2_record_3b_642 = {
            'jenis_data': 'Kartu Rencana Studi (KRS)',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_2_record_3b_642)]})

        line_3_record_3b_642 = {
            'jenis_data': 'Jadwal Mata Kuliah',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_3_record_3b_642)]})

        line_4_record_3b_642 = {
            'jenis_data': 'Nilai Mata Kuliah',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_4_record_3b_642)]})

        line_5_record_3b_642 = {
            'jenis_data': 'Transkrip Akademik',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_5_record_3b_642)]})

        line_6_record_3b_642 = {
            'jenis_data': 'Lulusan',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_6_record_3b_642)]})

        line_7_record_3b_642 = {
            'jenis_data': 'Dosen',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_7_record_3b_642)]})

        line_8_record_3b_642 = {
            'jenis_data': 'Pegawai',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_8_record_3b_642)]})

        line_9_record_3b_642 = {
            'jenis_data': 'Keuangan',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_9_record_3b_642)]})

        line_10_record_3b_642 = {
            'jenis_data': 'Inventaris',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_10_record_3b_642)]})

        line_11_record_3b_642 = {
            'jenis_data': 'Pembayaran SPP',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_11_record_3b_642)]})

        line_12_record_3b_642 = {
            'jenis_data': 'Perpustakaan',
            'pengolahan_data_manual': '',
            'pengolahan_data_komputer_tanpa_jaringan': '',
            'pengolahan_data_komputer_dengan_lan': '',
            'pengolahan_data_komputer_jaringan_luas': 'checklist',
        }
        report.write({'record_3b_642': [(0, 0, line_12_record_3b_642)]})
