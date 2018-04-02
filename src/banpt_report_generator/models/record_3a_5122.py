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
    pass
