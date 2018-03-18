# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_A3_3_1(models.Model):
    _name = 'banpt_report_generator.A3_3_1'
    _rec_name = 'nama'
    _title = 'A3_3_1'

    no = fields.Integer(string='No.')
    jenis_kemampuan = fields.Text(string='Jenis Kemampuan')
    tanggapan_sangat_baik = fields.Float(string='Sangat Baik')
    tanggapan_baik = fields.Float(string='Baik')
    tanggapan_cukup = fields.Float(string='Cukup')
    tanggapan_kurang = fields.Float(string='Kurang')
    rencana_tindak_lanjut_prodi = fields.Text(string='Rencana Tindak Lanjut oleh Program Studi')

    #A3_3_2
    avg_tunggu_pekerjaan_lulusan = fields.Float(string='Rata-rata waktu tunggu lulusan untuk memperoleh pekerjaan yang pertama')

    #A3_3_3
    persen_lulusan_pekerjaan_sesuai = fields.Float(string='Persentase lulusan yang bekerja pada bidang yang sesuai dengan keahliannya')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')
