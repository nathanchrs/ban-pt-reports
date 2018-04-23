# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Teknik Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    catalog_1 = context.env['itb.academic_catalog'].create(dict(
        name='Catalog 1',
        code='code1',
        credit=4
    ))

    catalog_2 = context.env['itb.academic_catalog'].create(dict(
        name='Catalog 2',
        code='code2',
        credit=3
    ))

    catalog_3 = context.env['itb.academic_catalog'].create(dict(
        name='Catalog 3',
        code='code3',
        credit=2
    ))

    catalog_4 = context.env['itb.academic_catalog'].create(dict(
        name='Catalog 4',
        code='code4',
        credit=1
    ))

    curriculum_1 = context.env['itb.academic_curriculum'].create(dict(
        name='Curriculum 1',
        year=2015,
        program_id=prodi_if.id,
        curriculum_line_ids=True
    ))

    context.env['itb.academic_curriculum_line'].create(dict(
        curriculum_id=curriculum_1.id,
        catalog_id=catalog_1.id,
        category='wajib',
        semester=1
    ))

    context.env['itb.academic_curriculum_line'].create(dict(
        curriculum_id=curriculum_1.id,
        catalog_id=catalog_2.id,
        category='opsional',
        semester=1
    ))

    context.env['itb.academic_curriculum_line'].create(dict(
        curriculum_id=curriculum_1.id,
        catalog_id=catalog_3.id,
        category='opsional-luar',
        semester=1
    ))

    context.env['itb.academic_curriculum_line'].create(dict(
        curriculum_id=curriculum_1.id,
        catalog_id=catalog_4.id,
        category='opsional-external',
        semester=1
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1',
        year=2015,
        refresh_date='2015-03-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_5121(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        ts_1 = report_1.record_3a_5121.search([['jenis_mata_kuliah', '=', 'Wajib']])
        self.assertEqual(ts_1.jenis_mata_kuliah, 'Wajib')
        self.assertEqual(ts_1.sks, 4)
        self.assertEqual(ts_1.keterangan, '')

        ts_2 = report_1.dosen.search([['jenis_mata_kuliah', '=', 'Pilihan']])
        self.assertEqual(ts_2.jenis_mata_kuliah, 'Pilihan')
        self.assertEqual(ts_2.sks, 6)
        self.assertEqual(ts_2.keterangan, '')
