# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_721(models.Model):
    _name = 'banpt_report_generator.record_3b_721'
    _rec_name = 'program_studi'
    _title = '3B-7.2.1 Kegiatan Pelayanan/Pengabdian kepada Masyarakat'

    program_studi = fields.Text(string='Nama Program Studi', required=True)
    jumlah_judul_kegiatan_masyarakat_ts_2 = fields.Text(string='Jumlah Judul Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-2', required=True)
    jumlah_judul_kegiatan_masyarakat_ts_1 = fields.Text(string='Jumlah Judul Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-1', required=True)
    jumlah_judul_kegiatan_masyarakat_ts = fields.Text(string='Jumlah Judul Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS', required=True)
    total_dana_kegiatan_masyarakat_ts_2 = fields.Integer(string='Total Dana Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-2 (juta rupiah)')
    total_dana_kegiatan_masyarakat_ts_1 = fields.Integer(string='Total Dana Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-1 (juta rupiah)')
    total_dana_kegiatan_masyarakat_ts = fields.Integer(string='Total Dana Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    pass
    