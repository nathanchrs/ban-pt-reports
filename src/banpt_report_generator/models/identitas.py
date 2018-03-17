# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_Identitas(models.Model):
    _name = 'banpt_report_generator.identitas'
    _rec_name = 'nama_prodi'
    _title = 'Identitas Prodi'

    nama_prodi = fields.Char(string='Nama prodi', required=True)
    departemen = fields.Char(string='Departemen')
    fakultas = fields.Char(string='Fakultas')
    perguruan_tinggi = fields.Char(string='Perguruan tinggi', required=True)

    nomor_sk_pendirian = fields.Char(string='Nomor SK pendirian')
    tanggal_sk_pendirian = fields.Date(string='Tanggal SK pendirian')
    pejabat_sk_pendirian = fields.Char(string='Pejabat SK pendirian')
    tanggal_penyelenggaraan = fields.Date(string='Tanggal penyelenggaraan')
    nomor_sk_izin_operasional = fields.Char(string='Nomor SK izin operasional')
    tanggal_sk_izin_operasional = fields.Date(string='Tanggal SK izin operasional')
    peringkat_akreditasi_ban_pt = fields.Char(string='Peringkat akreditasi BAN-PT')
    nilai_akreditasi_ban_pt = fields.Integer(string='Nilai akreditasi BAN-PT')
    nomor_sk_akreditasi_ban_pt = fields.Char(string='Nomor SK akreditasi BAN-PT')

    alamat = fields.Text(string='Alamat')
    telepon = fields.Char(string='Telepon')
    faks = fields.Char(string='Faks')
    homepage = fields.Char(string='Homepage')
    email = fields.Char(string='Email')
    
    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
