# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3B_642(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        ts_1 = report_1.record_3b_642.search([['jenis_data', '=', 'Mahasiswa']])
        self.assertEqual(ts_1.jenis_data, 'Mahasiswa')
        self.assertFalse(ts_1.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_1.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_1.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_1.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_2 = report_1.record_3b_642.search([['jenis_data', '=', 'Kartu Rencana Studi (KRS)']])
        self.assertEqual(ts_2.jenis_data, 'Kartu Rencana Studi (KRS)')
        self.assertFalse(ts_2.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_2.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_2.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_2.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_3 = report_1.record_3b_642.search([['jenis_data', '=', 'Jadwal Mata Kuliah']])
        self.assertEqual(ts_3.jenis_data, 'Jadwal Mata Kuliah')
        self.assertFalse(ts_3.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_3.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_3.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_3.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_4 = report_1.record_3b_642.search([['jenis_data', '=', 'Nilai Mata Kuliah']])
        self.assertEqual(ts_4.jenis_data, 'Nilai Mata Kuliah')
        self.assertFalse(ts_4.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_4.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_4.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_4.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_5 = report_1.record_3b_642.search([['jenis_data', '=', 'Transkrip Akademik']])
        self.assertEqual(ts_5.jenis_data, 'Transkrip Akademik')
        self.assertFalse(ts_5.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_5.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_5.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_5.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_6 = report_1.record_3b_642.search([['jenis_data', '=', 'Lulusan']])
        self.assertEqual(ts_6.jenis_data, 'Lulusan')
        self.assertFalse(ts_6.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_6.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_6.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_6.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_7 = report_1.record_3b_642.search([['jenis_data', '=', 'Dosen']])
        self.assertEqual(ts_7.jenis_data, 'Dosen')
        self.assertFalse(ts_7.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_7.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_7.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_7.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_8 = report_1.record_3b_642.search([['jenis_data', '=', 'Pegawai']])
        self.assertEqual(ts_8.jenis_data, 'Pegawai')
        self.assertFalse(ts_8.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_8.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_8.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_8.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_9 = report_1.record_3b_642.search([['jenis_data', '=', 'Keuangan']])
        self.assertEqual(ts_9.jenis_data, 'Keuangan')
        self.assertFalse(ts_9.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_9.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_9.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_9.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_10 = report_1.record_3b_642.search([['jenis_data', '=', 'Inventaris']])
        self.assertEqual(ts_10.jenis_data, 'Inventaris')
        self.assertFalse(ts_10.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_10.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_10.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_10.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_11 = report_1.record_3b_642.search([['jenis_data', '=', 'Perpustakaan']])
        self.assertEqual(ts_11.jenis_data, 'Perpustakaan')
        self.assertFalse(ts_11.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_11.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_11.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_11.pengolahan_data_komputer_jaringan_luas, 'checklist')

        ts_12 = report_1.record_3b_642.search([['jenis_data', '=', 'Pembayaran SPP']])
        self.assertEqual(ts_12.jenis_data, 'Pembayaran SPP')
        self.assertFalse(ts_12.pengolahan_data_manual, 'checklist')
        self.assertFalse(ts_12.pengolahan_data_komputer_tanpa_jaringan, 'checklist')
        self.assertFalse(ts_12.pengolahan_data_komputer_dengan_lan, 'checklist')
        self.assertEqual(ts_12.pengolahan_data_komputer_jaringan_luas, 'checklist')
