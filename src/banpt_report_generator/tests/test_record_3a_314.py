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

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13511001', graduate_date='2015-07-23'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13511101', graduate_date='2015-07-25'))

    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13510001', graduate_date='2013-10-23'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13510101', graduate_date='2014-07-25'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13510002', graduate_date='2014-07-23'))
    context.env['res.partner'].create(dict(name='Test', is_participant=True, student_id='13510102', graduate_date='2014-07-25'))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1',
        year=2016,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_314(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        self.assertFalse(report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-7']]))

        ts_6 = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-6']])
        self.assertEqual(ts_6.ts6, 4)
        self.assertEqual(ts_6.ts5, 4)
        self.assertEqual(ts_6.ts4, 4)
        self.assertEqual(ts_6.ts3, 4)
        self.assertEqual(ts_6.ts2, 3)
        self.assertEqual(ts_6.ts1, 0)
        self.assertEqual(ts_6.ts, 0)
        self.assertEqual(ts_6.lulusan_reguler_sampai_ts, 4)

        ts_5 = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-5']])
        self.assertEqual(ts_5.ts6, 0)
        self.assertEqual(ts_5.ts5, 2)
        self.assertEqual(ts_5.ts4, 2)
        self.assertEqual(ts_5.ts3, 2)
        self.assertEqual(ts_5.ts2, 2)
        self.assertEqual(ts_5.ts1, 2)
        self.assertEqual(ts_5.ts, 0)
        self.assertEqual(ts_5.lulusan_reguler_sampai_ts, 2)

        ts_4 = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-4']])
        self.assertEqual(ts_4.ts6, 0)
        self.assertEqual(ts_4.ts5, 0)
        self.assertEqual(ts_4.ts4, 2)
        self.assertEqual(ts_4.ts3, 2)
        self.assertEqual(ts_4.ts2, 2)
        self.assertEqual(ts_4.ts1, 2)
        self.assertEqual(ts_4.ts, 2)
        self.assertEqual(ts_4.lulusan_reguler_sampai_ts, 2)

        ts_3 = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-3']])
        self.assertEqual(ts_3.ts6, 0)
        self.assertEqual(ts_3.ts5, 0)
        self.assertEqual(ts_3.ts4, 0)
        self.assertEqual(ts_3.ts3, 7)
        self.assertEqual(ts_3.ts2, 7)
        self.assertEqual(ts_3.ts1, 7)
        self.assertEqual(ts_3.ts, 6)
        self.assertEqual(ts_3.lulusan_reguler_sampai_ts, 2)

        ts_2 = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-2']])
        self.assertEqual(ts_2.ts6, 0)
        self.assertEqual(ts_2.ts5, 0)
        self.assertEqual(ts_2.ts4, 0)
        self.assertEqual(ts_2.ts3, 0)
        self.assertEqual(ts_2.ts2, 4)
        self.assertEqual(ts_2.ts1, 4)
        self.assertEqual(ts_2.ts, 4)
        self.assertEqual(ts_2.lulusan_reguler_sampai_ts, 0)

        ts_1 = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS-1']])
        self.assertEqual(ts_1.ts6, 0)
        self.assertEqual(ts_1.ts5, 0)
        self.assertEqual(ts_1.ts4, 0)
        self.assertEqual(ts_1.ts3, 0)
        self.assertEqual(ts_1.ts2, 0)
        self.assertEqual(ts_1.ts1, 3)
        self.assertEqual(ts_1.ts, 3)
        self.assertEqual(ts_1.lulusan_reguler_sampai_ts, 0)

        ts = report_1.record_3a_314.search([['report', '=', report_1.id], ['tahun_masuk', '=', 'TS']])
        self.assertEqual(ts.ts6, 0)
        self.assertEqual(ts.ts5, 0)
        self.assertEqual(ts.ts4, 0)
        self.assertEqual(ts.ts3, 0)
        self.assertEqual(ts.ts2, 0)
        self.assertEqual(ts.ts1, 0)
        self.assertEqual(ts.ts, 2)
        self.assertEqual(ts.lulusan_reguler_sampai_ts, 0)
