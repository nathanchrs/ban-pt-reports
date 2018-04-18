# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    prodi_el = context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='182', degree='s1', active=True
    ))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13212001'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13213002'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13214601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13215602'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13216802'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13216202'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516001'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516002'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516602'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516801'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516802'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515002'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515013'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515123'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515273'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515813'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13514001'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13514101'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13514123'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13514212'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13514601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13514602'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513001', graduate_date='2017-10-23', ipk=3.50))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513004', graduate_date='2017-07-12', ipk=3.72))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513105', graduate_date='2017-07-29', ipk=3.29))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513123', graduate_date='2017-10-23', ipk=3.90))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513212', graduate_date='2017-10-23', ipk=3.30))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513300', graduate_date='2016-10-23', ipk=3.15))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513301'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513302'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513801', graduate_date='2016-10-23', ipk=2.86))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513802', graduate_date='2017-06-30', ipk=3.22))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513803', graduate_date='2018-04-14', ipk=3.14))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512001', graduate_date='2016-07-23', ipk=3.22))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512101', graduate_date='2016-07-25', ipk=3.90))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512123', graduate_date='2016-10-12', ipk=3.25))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512212', graduate_date='2015-07-22', ipk=3.70))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512212'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512601', graduate_date='2017-04-03', ipk=2.90))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512602', graduate_date='2018-04-13', ipk=3.05))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1',
        year=2016,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_311(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        self.assertFalse(report_1.record_3a_311.search([['report', '=', report_1.id], ['tahun', '=', 'TS-5']]))

        ts_4 = report_1.record_3a_311.search([['report', '=', report_1.id], ['tahun', '=', 'TS-4']])
        self.assertEqual(ts_4.mahasiswa_baru_reguler, 5)
        self.assertEqual(ts_4.mahasiswa_baru_transfer, 2)
        self.assertEqual(ts_4.total_mahasiswa_reguler, 5)
        self.assertEqual(ts_4.total_mahasiswa_transfer, 2)
        self.assertEqual(ts_4.lulusan_reguler, 0)
        self.assertEqual(ts_4.lulusan_transfer, 0)
        self.assertEqual(ts_4.ipk_reguler_min, 0.0)
        self.assertEqual(ts_4.ipk_reguler_avg, 0.0)
        self.assertEqual(ts_4.ipk_reguler_max, 0.0)
        self.assertEqual(ts_4.persen_ipk_275, 0.0)
        self.assertEqual(ts_4.persen_ipk_275_350, 0.0)
        self.assertEqual(ts_4.persen_ipk_350, 0.0)

        ts_3 = report_1.record_3a_311.search([['report', '=', report_1.id], ['tahun', '=', 'TS-3']])
        self.assertEqual(ts_3.mahasiswa_baru_reguler, 8)
        self.assertEqual(ts_3.mahasiswa_baru_transfer, 0)
        self.assertEqual(ts_3.total_mahasiswa_reguler, 13)
        self.assertEqual(ts_3.total_mahasiswa_transfer, 2)
        self.assertEqual(ts_3.lulusan_reguler, 0)
        self.assertEqual(ts_3.lulusan_transfer, 0)
        self.assertEqual(ts_3.ipk_reguler_min, 0.0)
        self.assertEqual(ts_3.ipk_reguler_avg, 0.0)
        self.assertEqual(ts_3.ipk_reguler_max, 0.0)
        self.assertEqual(ts_3.persen_ipk_275, 0.0)
        self.assertEqual(ts_3.persen_ipk_275_350, 0.0)
        self.assertEqual(ts_3.persen_ipk_350, 0.0)

        ts_2 = report_1.record_3a_311.search([['report', '=', report_1.id], ['tahun', '=', 'TS-2']])
        self.assertEqual(ts_2.mahasiswa_baru_reguler, 4)
        self.assertEqual(ts_2.mahasiswa_baru_transfer, 2)
        self.assertEqual(ts_2.total_mahasiswa_reguler, 17)
        self.assertEqual(ts_2.total_mahasiswa_transfer, 4)
        self.assertEqual(ts_2.lulusan_reguler, 0)
        self.assertEqual(ts_2.lulusan_transfer, 0)
        self.assertEqual(ts_2.ipk_reguler_min, 0.0)
        self.assertEqual(ts_2.ipk_reguler_avg, 0.0)
        self.assertEqual(ts_2.ipk_reguler_max, 0.0)
        self.assertEqual(ts_2.persen_ipk_275, 0.0)
        self.assertEqual(ts_2.persen_ipk_275_350, 0.0)
        self.assertEqual(ts_2.persen_ipk_350, 0.0)

        ts_1 = report_1.record_3a_311.search([['report', '=', report_1.id], ['tahun', '=', 'TS-1']])
        self.assertEqual(ts_1.mahasiswa_baru_reguler, 4)
        self.assertEqual(ts_1.mahasiswa_baru_transfer, 1)
        self.assertEqual(ts_1.total_mahasiswa_reguler, 21)
        self.assertEqual(ts_1.total_mahasiswa_transfer, 5)
        self.assertEqual(ts_1.lulusan_reguler, 1)
        self.assertEqual(ts_1.lulusan_transfer, 0)
        self.assertEqual(ts_1.ipk_reguler_min, 3.70)
        self.assertEqual(ts_1.ipk_reguler_avg, 3.70)
        self.assertEqual(ts_1.ipk_reguler_max, 3.70)
        self.assertEqual(ts_1.persen_ipk_275, 0.0)
        self.assertEqual(ts_1.persen_ipk_275_350, 0.0)
        self.assertEqual(ts_1.persen_ipk_350, 100.0)

        ts = report_1.record_3a_311.search([['report', '=', report_1.id], ['tahun', '=', 'TS']])
        self.assertEqual(ts.mahasiswa_baru_reguler, 2)
        self.assertEqual(ts.mahasiswa_baru_transfer, 2)
        self.assertEqual(ts.total_mahasiswa_reguler, 22)
        self.assertEqual(ts.total_mahasiswa_transfer, 7)
        self.assertEqual(ts.lulusan_reguler, 4)
        self.assertEqual(ts.lulusan_transfer, 0)
        self.assertEqual(ts.ipk_reguler_min, 3.15)
        self.assertEqual(ts.ipk_reguler_avg, 3.38)
        self.assertEqual(ts.ipk_reguler_max, 3.90)
        self.assertEqual(ts.persen_ipk_275, 0.0)
        self.assertEqual(ts.persen_ipk_275_350, 75.0)
        self.assertEqual(ts.persen_ipk_350, 25.0)
