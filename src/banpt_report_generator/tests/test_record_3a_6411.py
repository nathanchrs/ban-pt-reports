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

class TestRecord_3A_6411(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        ts_1 = report_1.record_3a_6411.search([['jenis_pustaka', '=', 'Buku Teks']])
        self.assertEqual(ts_1.jenis_pustaka, 'Buku Teks')
        self.assertEqual(ts_1.jumlah_judul, 3762)
        self.assertEqual(ts_1.jumlah_copy, 9140)

        ts_2 = report_1.record_3a_6411.search([['jenis_pustaka', '=', 'Jurnal Nasional Yang Terakreditasi']])
        self.assertEqual(ts_2.jenis_pustaka, 'Jurnal Nasional Yang Terakreditasi')
        self.assertEqual(ts_2.jumlah_judul, 6)
        self.assertEqual(ts_2.jumlah_copy, 0)

        ts_3 = report_1.record_3a_6411.search([['jenis_pustaka', '=', 'Jurnal Internasional']])
        self.assertEqual(ts_3.jenis_pustaka, 'Jurnal Internasional')
        self.assertEqual(ts_3.jumlah_judul, 18)
        self.assertEqual(ts_3.jumlah_copy, 0)

        ts_4 = report_1.record_3a_6411.search([['jenis_pustaka', '=', 'Prosiding']])
        self.assertEqual(ts_4.jenis_pustaka, 'Prosiding')
        self.assertEqual(ts_4.jumlah_judul, 48)
        self.assertEqual(ts_4.jumlah_copy, 0)

        ts_5 = report_1.record_3a_6411.search([['jenis_pustaka', '=', 'Skripsi/Tesis']])
        self.assertEqual(ts_5.jenis_pustaka, 'Skripsi/Tesis')
        self.assertEqual(ts_5.jumlah_judul, 6)
        self.assertEqual(ts_5.jumlah_copy, 0)

        ts_6 = report_1.record_3a_6411.search([['jenis_pustaka', '=', 'Disertasi']])
        self.assertEqual(ts_6.jenis_pustaka, 'Disertasi')
        self.assertEqual(ts_6.jumlah_judul, 21)
        self.assertEqual(ts_6.jumlah_copy, 30)
