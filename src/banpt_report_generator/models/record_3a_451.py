# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_451(models.Model):
    _name = 'banpt_report_generator.record_3a_451'
    _rec_name = 'nama'
    _title = '3A-4.5.1 Kegiatan Tenaga Ahli/Pakar (Tidak Termasuk Dosen Tetap)'

    no = fields.Integer(string='No.')
    nama = fields.Char(string='Nama Tenaga Ahli/Pakar')
    instansi = fields.Char(string='Instansi/Jabatan')
    nama_kegiatan = fields.Char(string='Nama dan Judul Kegiatan')
    tanggal_pelaksanaan = fields.Date(string='Tanggal Pelaksanaan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_451.unlink()

        # TODO: add refresh method
        new_record_3a_451 = {
            'no': 1, # TODO: default value just for dummy
            'nama': 'Not Found', # TODO: default value just for dummy
            'instansi': 'Not Found', # TODO: default value just for dummy
            'nama_kegiatan': 'Not Found', # TODO: default value just for dummy
        }

        report.write({'record_3a_451': [(0, 0, new_record_3a_451)]})
