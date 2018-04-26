# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    rec_3a_451 = context.env['banpt_report_generator.record_3a_451'].create(dict(
        no=5,
        nama='Jaka Widada',
        instansi='Istana Kepresidenan',
        nama_kegiatan='Kuliah Umum Socio-Informatika',
        tanggal_pelaksanaan='2014-10-05'
    ))

    return rec_3a_451

class TestRecord_3A_451(common.TransactionCase):
    def test_refresh(self):
        rec_3a_451 = seed(self)

        kegiatan_1_test = rec_3a_451.search([['no', '=', 5]])
        self.assertEqual(kegiatan_1_test.no, 5)
        self.assertEqual(kegiatan_1_test.nama, 'Jaka Widada')
        self.assertEqual(kegiatan_1_test.instansi, 'Istana Kepresidenan')
        self.assertEqual(kegiatan_1_test.nama_kegiatan, 'Kuliah Umum Socio-Informatika')
        self.assertEqual(kegiatan_1_test.tanggal_pelaksanaan, '2014-10-05')
