# -*- coding: utf-8 -*-

from odoo.tests import common
from . import testutils

def seed_report_1(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    report_1 = dict(
        name='Sample Report 1',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    )

    return context.env['banpt_report_generator.report'].create(report_1)

class TestReport(common.TransactionCase):
    def test_write_and_approve(self):
        record = seed_report_1(self)
        self.assertEqual(record.state, 'pending_review')

        record.approve()
        self.assertEqual(record.state, 'approved')

        record.approve()
        self.assertEqual(record.state, 'approved')

        record.write({'name': 'Sample Report 1 edited'})
        self.assertEqual(record.state, 'pending_review')

        record.approve()
        self.assertEqual(record.state, 'approved')

    def test_refresh(self):
        record = seed_report_1(self)
        record.refresh()
        self.assertGreater(
            testutils.parse_datetime(record.refresh_date),
            testutils.n_mins_before_now(1)
        )
