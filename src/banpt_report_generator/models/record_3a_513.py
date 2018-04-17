# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_513(models.Model):
    _name = 'banpt_report_generator.record_3a_513'
    _rec_name = 'kode_mk'
    _title = '3A-5.1.3 Mata Kuliah Pilihan'

    smt = fields.Text(string='Semester', required=True)
    kode_mk = fields.Char(string='Kode Mata Kuliah(pilihan)', required=True)
    nama_mk = fields.Text(string='Nama Mata Kuliah', required=True)
    bobot_sks = fields.Integer(string='Bobot SKS', required=True)
    bobot_tugas = fields.Char(string='Bobot Tugas')
    unit_penyelenggara = fields.Char(string='Unit/Jurusan/Fakultas Penyelenggara', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
