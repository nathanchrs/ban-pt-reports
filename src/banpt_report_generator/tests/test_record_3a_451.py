# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_451 = context.env['banpt_report_generator.record_3a_451'].create(dict(
        no=5,
        nama='Jaka Widada',
        instansi='Istana Kepresidenan',
        nama_kegiatan='Kuliah Umum Socio-Informatika',
        tanggal_pelaksanaan='2014-10-05'
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_451

class TestRecord_3A_451(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_451 = seed(self)

        report_1.refresh()

        kegiatan_1_test = rec_3a_451.search([['no', '=', 5]])
        self.assertEqual(kegiatan_1_test.no, 5)
        self.assertEqual(kegiatan_1_test.nama, 'Jaka Widada')
        self.assertEqual(kegiatan_1_test.instansi, 'Istana Kepresidenan')
        self.assertEqual(kegiatan_1_test.nama_kegiatan, 'Kuliah Umum Socio-Informatika')
        self.assertEqual(kegiatan_1_test.tanggal_pelaksanaan, '2014-10-05')

        kegiatan_2_test = report_1.record_3a_451.search([['no', '=', 1]])
        self.assertEqual(kegiatan_2_test.no, 1)
        self.assertEqual(kegiatan_2_test.nama, 'Not Found')
        self.assertEqual(kegiatan_2_test.instansi, 'Not Found')
        self.assertEqual(kegiatan_2_test.nama_kegiatan, 'Not Found')
        self.assertFalse(kegiatan_2_test.tanggal_pelaksanaan, '')
