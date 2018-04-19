# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))
    context.env['itb.academic_program'].create(dict(
        name='Teknik Elektro', name_en='Electrical Engineering', prefix='182', degree='s1', active=True
    ))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13212001'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13212803'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13213002'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13214601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13215602'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13216802'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13216803'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516001'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516002'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516602'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516801'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13516802'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515013'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515123'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515273'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515601'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13515812'))
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
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513212', graduate_date='2015-10-23', ipk=3.30))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513300', graduate_date='2016-10-23', ipk=3.15))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513301'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513801', graduate_date='2016-10-23'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513802', graduate_date='2015-06-30'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513803', graduate_date='2018-04-14'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13513804'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512001', graduate_date='2016-07-23'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512101', graduate_date='2016-07-25'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512601', graduate_date='2017-04-03'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512602', graduate_date='2014-04-13'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512623', graduate_date='2015-10-12'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512812', graduate_date='2015-07-22'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13512815'))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1',
        year=2016,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_312(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        self.assertFalse(report_1.record_3a_312.search([['report', '=', report_1.id], ['tahun', '=', 'TS-5']]))

        ts_4 = report_1.record_3a_312.search([['report', '=', report_1.id], ['tahun', '=', 'TS-4']])
        self.assertEqual(ts_4.mahasiswa_baru_nonreguler, 2)
        self.assertEqual(ts_4.mahasiswa_baru_transfer, 3)
        self.assertEqual(ts_4.total_mahasiswa_nonreguler, 2)
        self.assertEqual(ts_4.total_mahasiswa_transfer, 3)

        ts_3 = report_1.record_3a_312.search([['report', '=', report_1.id], ['tahun', '=', 'TS-3']])
        self.assertEqual(ts_3.mahasiswa_baru_nonreguler, 4)
        self.assertEqual(ts_3.mahasiswa_baru_transfer, 0)
        self.assertEqual(ts_3.total_mahasiswa_nonreguler, 6)
        self.assertEqual(ts_3.total_mahasiswa_transfer, 3)

        ts_2 = report_1.record_3a_312.search([['report', '=', report_1.id], ['tahun', '=', 'TS-2']])
        self.assertEqual(ts_2.mahasiswa_baru_nonreguler, 0)
        self.assertEqual(ts_2.mahasiswa_baru_transfer, 2)
        self.assertEqual(ts_2.total_mahasiswa_nonreguler, 6)
        self.assertEqual(ts_2.total_mahasiswa_transfer, 5)

        ts_1 = report_1.record_3a_312.search([['report', '=', report_1.id], ['tahun', '=', 'TS-1']])
        self.assertEqual(ts_1.mahasiswa_baru_nonreguler, 2)
        self.assertEqual(ts_1.mahasiswa_baru_transfer, 1)
        self.assertEqual(ts_1.total_mahasiswa_nonreguler, 8)
        self.assertEqual(ts_1.total_mahasiswa_transfer, 5)

        ts = report_1.record_3a_312.search([['report', '=', report_1.id], ['tahun', '=', 'TS']])
        self.assertEqual(ts.mahasiswa_baru_nonreguler, 2)
        self.assertEqual(ts.mahasiswa_baru_transfer, 2)
        self.assertEqual(ts.total_mahasiswa_nonreguler, 8)
        self.assertEqual(ts.total_mahasiswa_transfer, 6)
